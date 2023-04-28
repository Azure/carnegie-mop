All data files use tab ('\t') as delimiter.

### Text Modality

- data column(required): text
- data value: it should be one text without line break. **SHOULD NOT** be Null/NaN/empty.
- label columns (required. Support multiple label columns but no duplicate, at least one label): hate, violent
- label value: it should be one of 0(negative) or 1(positive).
- All columns should have the same number of rows.

### ImageAndText Modality

- data column(required): text
- data value: it should be one text without line break. Each image should be represented by a placeholder as ##{image_column_name} like ##{image_0}. No Null/NaN/empty in text value.
- image column(optional): image_0, image_1, image_2, ……, image_19
- image value: base64 string of image which appears in text value as ##{image_column_name}. It can be null/na only when this image column name doesn't appear in text value.
- label column(required. Support multiple label columns but no duplicate, at least one label): hate, violent
- label value: it should be one of 0(negative) or 1(positive).

### Image Modality

- data column(required): base64_image, file_name, image_width_pixels, image_height_pixels
- data value: base64 encoded string of the image, file name with extension, image_width_pixels and image_height_pixels should be positive integer, no Null/NaN/empty.
- label column(optional. Support multiple label columns but no duplicate, at least one label): hate, violent
- label value: it should be one of 0(negative) or 1(positive).
- All columns should have the same number of rows.
