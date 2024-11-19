import random
from io import BytesIO
from typing import List

from PIL import Image
from django.conf import settings
from django.core.files.base import ContentFile
from django.db.models import QuerySet

from apps.data.choices import TrainingElementMeterType, TrainingElementPositionType
from apps.data.exceptions import NotEnoughElementsException, MaxOptionsException
from apps.data.models import TrainingElement, TrainingAugmentation
from django.utils.translation import gettext_lazy as _


class CreateAugmentationData:
    MIN_START_ELEMENT = 1
    MIN_MIDDLE_ELEMENT = 1
    MIN_END_ELEMENT = 1
    MIN_ELEMENTS_COUNT = 3
    MAX_ELEMENTS_COUNT = 5

    def _get_elements(self, augmentation_type: TrainingElementMeterType) -> tuple[QuerySet[TrainingElement], QuerySet[TrainingElement], QuerySet[TrainingElement]]:
        start_elements = TrainingElement.objects.filter(
            type=augmentation_type, number_type=TrainingElementPositionType.START.value
        ).only('id', 'image', 'correct_value')
        middle_elements = TrainingElement.objects.filter(
            type=augmentation_type, number_type=TrainingElementPositionType.MIDDLE.value
        ).only('id', 'image', 'correct_value')
        end_elements = TrainingElement.objects.filter(
            type=augmentation_type, number_type=TrainingElementPositionType.END.value
        ).only('id', 'image', 'correct_value')
        return start_elements, middle_elements, end_elements

    def _check_elements_count(self, start_elements_count: int, middle_elements_count: int, end_elements_count: int, number_images: int, augmentation_type: TrainingElementMeterType) -> None:
        """
        This method checks if there are enough elements to generate unique images
        It helps manage the image generation process, ensuring that the request to generate a certain number of
            images does not exceed what can actually be produced with the available elements
        The method calculates the approximate number of unique images that can be generated using the given elements.
            It issues exceptions if there are not enough elements to fulfill the minimum requirements or if
            he requested number exceeds the approximate possible variants
        """
        if start_elements_count < self.MIN_START_ELEMENT or middle_elements_count < self.MIN_END_ELEMENT or end_elements_count < self.MIN_END_ELEMENT:
            raise NotEnoughElementsException()

        max_variants = start_elements_count * middle_elements_count * end_elements_count

        augmentation_count = TrainingAugmentation.objects.filter(type=augmentation_type).count()

        if number_images + augmentation_count > max_variants:
            raise MaxOptionsException(message=_(
                f"the maximum number of elements available for generation is {max_variants - augmentation_count}"
            ))

    def _get_random_elements(
        self, start_elements: QuerySet[TrainingElement], middle_elements: QuerySet[TrainingElement],
        end_elements: QuerySet[TrainingElement], augmentation_type: TrainingElementMeterType
    ) -> List[TrainingElement]:
        """
        This method is a random training element selector from specified groups
        It is used to compile a unique set of learning elements for later sew
        """
        elements_count = random.randint(self.MIN_ELEMENTS_COUNT, self.MAX_ELEMENTS_COUNT)

        selected_elements = []
        selected_elements.append(random.choice(start_elements))
        selected_elements.extend(random.choices(middle_elements, k=elements_count - 2))
        selected_elements.append(random.choice(end_elements))

        selected_ids = sorted([element.id for element in selected_elements])
        training_aug_exists = TrainingAugmentation.objects.filter(type=augmentation_type, training_element_ids=selected_ids).exists()
        if training_aug_exists:
            return self._get_random_elements(
                start_elements=start_elements,
                middle_elements=middle_elements,
                end_elements=end_elements,
                augmentation_type=augmentation_type
            )

        return selected_elements

    def _resize_images(self, images: List[Image.Image]) -> List[Image.Image]:
        """
        Resizes a list of images to a specified height while maintaining the aspect ratio
        """
        resized_images = []
        for img in images:
            new_width = int(img.width * settings.IMAGE_SIZE_Y / img.height)
            resized_img = img.resize((new_width, settings.IMAGE_SIZE_Y), Image.Resampling.LANCZOS)
            resized_images.append(resized_img)

        return resized_images

    def _stitch_images(self, images: List[Image.Image]) -> Image.Image:
        """
        Stitch images together horizontally
        """
        total_width = sum(img.width for img in images)
        max_height = max(img.height for img in images)

        stitched_image = Image.new('RGB', (total_width, max_height))

        current_x = 0
        for img in images:
            stitched_image.paste(img, (current_x, 0))
            current_x += img.width

        return stitched_image

    def _resize_final_image(self, stitched_image: Image.Image) -> Image.Image:
        """
        Resize the final stitched image to the specified dimensions
        """
        final_image = stitched_image.resize((settings.IMAGE_SIZE_X, settings.IMAGE_SIZE_Y), Image.Resampling.LANCZOS)
        return final_image

    def _combine_correct_values(self, elements: List[TrainingElement]) -> str:
        """
        Combine correct values of the given elements into a single string.
        """
        combined_value = "".join(element.correct_value for element in elements)
        return combined_value

    def _save_image_to_field(self, image: Image.Image) -> ContentFile:
        """
        Save a PIL image to a Django ImageField.
        """
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        return ContentFile(buffer.getvalue(), name='augmentation.png')

    def generate_augmentations(self, augmentation_type: TrainingElementMeterType, number_images: int):
        start_elements, middle_elements, end_elements = self._get_elements(augmentation_type=augmentation_type)

        self._check_elements_count(
            start_elements_count=len(start_elements),
            middle_elements_count=len(middle_elements),
            end_elements_count=len(end_elements),
            number_images=number_images,
            augmentation_type=augmentation_type
        )

        for number_image in range(number_images):
            print(f"{number_image + 1}/{number_images}")

            elements = self._get_random_elements(
                start_elements=start_elements,
                middle_elements=middle_elements,
                end_elements=end_elements,
                augmentation_type=augmentation_type
            )

            images = [Image.open(element.image.path) for element in elements]
            images = self._resize_images(images=images)

            stitched_image = self._stitch_images(images)
            stitched_image = self._resize_final_image(stitched_image=stitched_image)
            stitched_image = self._save_image_to_field(stitched_image)

            correct_value = self._combine_correct_values(elements=elements)

            TrainingAugmentation.objects.create(
                image=stitched_image,
                type=augmentation_type,
                correct_value=float(correct_value),
                training_element_ids=[element.id for element in elements]
            )
