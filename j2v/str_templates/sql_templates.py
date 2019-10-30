join_str_template = "LATERAL FLATTEN(OUTER => TRUE, INPUT => {exploded_structure_path}) {alias}"
field_str_template = "{TABLE}.{path}::{json_type} AS {path_alias}"
non_nullable_text_field_str_template = "IFNULL({TABLE}.{path}::{json_type},'N/A') AS {path_alias}"
non_nullable_numeric_field_str_template = "IFNULL({TABLE}.{path}::{json_type},0) AS {path_alias}"
