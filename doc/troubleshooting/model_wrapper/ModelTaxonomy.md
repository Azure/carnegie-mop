# Model Taxonomy

## 1. TaxonomyMisMatchError
### A simplified description might resemble the following:
```html
Taxonomy=<taxonomy> not returned. model_revision_uuid = <model_revision_uuid>
```
### Take appropriate action:
- Ensure that the taxonomy matches the taxonomies in the response. For instance, the taxonomy should match 'identity_hate' in the API '/score' response.  
    - The example sentence emphasizes the specific matching requirement. The taxonomy mapping may appear as follows:  
![img.png](images/TaxonomyMisMatchError.png)