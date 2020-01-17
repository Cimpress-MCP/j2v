dimension_str_template = """
  dimension: {dimension_name} {{
    label: \"{dimension_label}\"
    description: \"{desc}\"{primary_key_field}
    type: {looker_type}
    sql: ${{TABLE}}.{path}::{json_type} ;;{group_label_string}
  }}
    """

dimension_group_time_template = """
  dimension_group: {dimension_name} {{
    description: \"{desc}\"{data_type_field}
    type: {looker_type}
    timeframes: [
        raw,
        time,
        date,
        week,
        month,
        quarter,
        year
    ]
    sql: ${{TABLE}}.{path}::{json_type} ;;
  }}
    """

view_start_str_template = """
view: {name} {{ {base_table}
  label: \"{label}"\
"""

view_end_str = """
}
"""

explore_start_str_template = """include: "{view_file_name}"
   
explore: {explore_name} {{
  view_name: {base_view_alias}
  from: {base_view}
  label: "{label}"
  description: "{description}"
"""

explore_join_str_template = """
  join: {alias} {{
     from: {view}
     sql:,{join_expression};;
     relationship: one_to_many {required_joins_line}
  }}
  """

req_joins_str_template = """
     required_joins: [{required_join}]"""

explore_end = """
}
"""

invalid_dim_name_regex = '[^0-9a-z_A-Z]+'
