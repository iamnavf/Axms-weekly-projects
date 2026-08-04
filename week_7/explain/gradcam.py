import os
import cv2
import numpy as np
import tensorflow as tf

from tensorflow.keras.models import load_model


class GradCAM:

    def __init__(self, model_path, last_conv_layer_name=None, input_shape=(224, 224, 3)):

        self.model = load_model(model_path)

        if last_conv_layer_name is None:
            self.last_conv_layer_name = self._find_last_conv_layer_name()
        else:
            self.last_conv_layer_name = last_conv_layer_name

   
        inputs = tf.keras.Input(shape=input_shape)
        x = inputs
        conv_output_tensor = None

        for layer in self.model.layers:
            x = layer(x)
            if layer.name == self.last_conv_layer_name:
                conv_output_tensor = x

        if conv_output_tensor is None:
            raise ValueError(
                f"Layer '{self.last_conv_layer_name}' not found while "
                f"rebuilding the functional graph."
            )

        self.grad_model = tf.keras.models.Model(
            inputs=inputs,
            outputs=[conv_output_tensor, x]
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

    def _find_last_conv_layer_name(self):
        for layer in reversed(self.model.layers):
            if isinstance(layer, tf.keras.layers.Conv2D):
                return layer.name
        raise ValueError("No Conv2D layer found in model.")

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
       
        image = self.preprocess(image_path)

        with tf.GradientTape() as tape:

            conv_outputs, predictions = self.grad_model(image)

            tape.watch(conv_outputs)

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

        weight = (heatmap * alpha)[..., np.newaxis]

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

        return {"prediction":self.class_names[predicted_class],
                "confidence":confidence,
                "probabilities":probabilities,
                "gradcam_path":save_path}