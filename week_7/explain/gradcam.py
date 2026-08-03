import os
import cv2
import numpy as np
import tensorflow as tf

from tensorflow.keras.models import load_model


class GradCAM:

    def __init__(self, model_path, last_conv_layer_name=None):

        # Load trained model
        self.model = load_model(model_path)

        # Sequential Model
        self.base_model = self.model.layers[0]

        # Classification head
        self.classifier = tf.keras.Sequential(
            self.model.layers[1:]
        )

  
        if last_conv_layer_name is None:
            try:
                self.last_conv_layer = self.base_model.get_layer("top_activation")
            except ValueError:
                self.last_conv_layer = self.base_model.get_layer("top_conv")
        else:
            self.last_conv_layer = self.base_model.get_layer(last_conv_layer_name)

  
        self.grad_model = tf.keras.models.Model(
            inputs=self.base_model.input,
            outputs=[
                self.last_conv_layer.output,
                self.base_model.output
            ]
        )

        self.class_names = [
            "Actinic Keratoses",
            "Basal Cell Carcinoma",
            "Benign Keratosis-like Lesions",
            "Dermatofibroma",
            "Melanoma",
            "Melanocytic Nevi",
            "Vascular Lesions"
        ]

    def preprocess(self, image_path):

        image = tf.io.read_file(image_path)

        image = tf.image.decode_jpeg(
            image,
            channels=3
        )

        image = tf.image.resize(
            image,
            (224, 224)
        )

  
        image = tf.cast(
            image,
            tf.float32
        ) / 255.0

        image = tf.expand_dims(
            image,
            axis=0
        )

        return image

    def generate(self, image_path, save_path, alpha=0.6, blur_ksize=15):
        """
        alpha: max blending strength at the hottest point of the heatmap.
        blur_ksize: Gaussian blur kernel used to smooth the (low-resolution)
                    heatmap before it's upscaled to the image size.
        """

        image = self.preprocess(image_path)

        with tf.GradientTape() as tape:

            # Forward pass through EfficientNet
            conv_outputs, features = self.grad_model(image)

            tape.watch(conv_outputs)

            # Forward pass through classifier head
            predictions = self.classifier(features)

            predicted_index = tf.argmax(predictions[0])

            loss = predictions[:, predicted_index]

        grads = tape.gradient(
            loss,
            conv_outputs
        )

        pooled_grads = tf.reduce_mean(
            grads,
            axis=(0, 1, 2)
        )

        conv_outputs = conv_outputs[0]

        heatmap = tf.reduce_sum(
            conv_outputs * pooled_grads,
            axis=-1
        )

        heatmap = tf.maximum(
            heatmap,
            0
        )

        heatmap = heatmap / (
            tf.reduce_max(heatmap) + 1e-8
        )

        heatmap = heatmap.numpy()

        original = cv2.imread(image_path)

        original = cv2.cvtColor(
            original,
            cv2.COLOR_BGR2RGB
        )

        heatmap = cv2.resize(
            heatmap,
            (original.shape[1], original.shape[0])
        )

        # Smooth the heatmap - Grad-CAM's native resolution is only 7x7
        # for EfficientNetB0, so upscaling it to a 224x224+ image without
        # smoothing gives blocky, unnatural-looking regions.
        if blur_ksize and blur_ksize > 1:
            k = blur_ksize if blur_ksize % 2 == 1 else blur_ksize + 1
            heatmap = cv2.GaussianBlur(heatmap, (k, k), 0)

        heatmap_uint8 = np.uint8(255 * heatmap)

        heatmap_color = cv2.applyColorMap(
            heatmap_uint8,
            cv2.COLORMAP_JET
        )

        heatmap_color = cv2.cvtColor(
            heatmap_color,
            cv2.COLOR_BGR2RGB
        )

    
        weight = (heatmap * alpha)[..., np.newaxis]  # (H, W, 1), 0..alpha

        overlay = (
            original.astype(np.float32) * (1 - weight)
            + heatmap_color.astype(np.float32) * weight
        )
        overlay = np.uint8(np.clip(overlay, 0, 255))

        os.makedirs(
            os.path.dirname(save_path),
            exist_ok=True
        )

        cv2.imwrite(
            save_path,
            cv2.cvtColor(
                overlay,
                cv2.COLOR_RGB2BGR
            )
        )

        prediction = predictions.numpy()[0]

        predicted_class = int(
            np.argmax(prediction)
        )

        confidence = float(
            np.max(prediction) * 100
        )

        probabilities = prediction.tolist()

        return {

            "prediction":
                self.class_names[predicted_class],

            "confidence":
                confidence,

            "probabilities":
                probabilities,

            "gradcam_path":
                save_path

        }