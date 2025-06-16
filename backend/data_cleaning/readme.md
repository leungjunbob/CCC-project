# Overview

The pipeline performs the following cleaning operations:
* Converts array fields to single values (except for 'tags')
* Creates a cleaned_content field from the original content
* Converts text to lowercase
* Removes HTML tags
* Removes punctuation marks
* Cleans up extra spaces

## Deployment Instructions

### Prerequisites
* Elasticsearch 7.x or higher
* Administrative access to the Elasticsearch cluster
* Kibana (optional, for using Dev Tools)

### Deployment Steps

1. Deploy the pipeline components in the following order:
   * scalable_convert_arrays
   * scalable_add_cleaned_content
   * scalable_to_lowercase
   * scalable_remove_html
   * scalable_remove_punctuation
   * scalable_clean_spaces
   * scalable_master_pipeline

2. (Optional) Create the destination index with predefined mappings

3. (Optional) Execute the reindex operation to process data

### Deployment Methods

You can deploy the pipelines using one of these methods:

1. **Using Kibana Dev Tools**
   * Open Kibana and navigate to Dev Tools
   * Copy and paste each command block from the pipeline file
   * Execute them in sequence

2. **Using Elasticsearch Client Libraries**
   * Use the appropriate client library for your programming language
   * Execute the same API calls as defined in the pipeline file