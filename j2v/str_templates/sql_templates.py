snowflake = {
    "ELEMENT_ACCESS_STR": "VALUE",
    "path_step": "\"{path_step}\"",
    "concat_steps": "{step1}:{step2}",
    "join_str_template": "LATERAL FLATTEN(OUTER => TRUE, INPUT => {exploded_structure_path}) {alias}",
    "field_str_template":"{TABLE}.{path}::{json_type} AS {path_alias}",
    "non_nullable_text_field_str_template": "IFNULL({TABLE}.{path}::{json_type},'N/A') AS {path_alias}",
    "non_nullable_numeric_field_str_template": "IFNULL({TABLE}.{path}::{json_type},0) AS {path_alias}",
    "join_separator": ",",
    "dimension_sql": "${{TABLE}}.{path}::{json_type} ;;{group_label_string}"
}

bigquery = {
    "ELEMENT_ACCESS_STR": "",
    "path_step": "{path_step}",
    "concat_steps": "{step1}.{step2}",
    "join_str_template": "LEFT JOIN UNNEST({exploded_structure_path}) AS {alias}",
    "field_str_template":"{TABLE}.{path} AS {path_alias}",
    "non_nullable_text_field_str_template": "IFNULL({TABLE}.{path},'N/A') AS {path_alias}",
    "non_nullable_numeric_field_str_template": "IFNULL({TABLE}.{path},0) AS {path_alias}",
    "join_separator": "",
    "dimension_sql": "${{TABLE}}.{path} ;;{group_label_string}"
}
