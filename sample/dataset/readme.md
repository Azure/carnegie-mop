All data file use comma(,) as delimiter.

### Text Modality

- data column(essential header): text
- data value: it should be one text without line break, no be Null/NaN/empty.
- label column(support multiple headers but no duplicate, at leaset one label): hate, violent
- label value: it should be one of 0(negative) or 1(positive).
- All columns should have the same number of rows.

### ImageAndText Modality

- data column(essential header): text
- data value: it should be one text withouut line break, any images should be typed as ##{image_header} like ##{image_0}, no Null/NaN/empty.
- image column(not essential header): image_0, image_1, image_2, ……, image_19
- image value: base64 string of image which appears in text value as ##{image_header}. It can be null/na only when this image header doesn't appeared in text value.
- label column(support multiple headers but no duplicate, at leaset one label): hate, violent
- label value: it should be one of 0(negative) or 1(positive).

### Image Modality

- data column(essential header): base64_image, file_name, image_width_pixels, image_height_pixels
- data value: base64 encoded string of the image, file name with extension, image_width_pixels and image_height_pixels should be positive integer, no Null/NaN/empty.
- label column(support multiple headers but no duplicate, at leaset one label): hate, violent
- label value: it should be one of 0(negative) or 1(positive).
- All columns should have the same number of rows.
