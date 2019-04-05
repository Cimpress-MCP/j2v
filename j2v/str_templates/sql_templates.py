join_str_template = "LATERAL FLATTEN(OUTER => TRUE, INPUT => {exploded_structure_path}) {alias}"
field_str_template = "{TABLE}.{__path}::{json_type}"
