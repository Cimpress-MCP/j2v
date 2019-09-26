
view: JSON_TABLE { 
  sql_table_name: session_info ;;

  dimension_group: received {
    description: "Received"
    type: time
    timeframes: [
        raw,
        time,
        date,
        week,
        month,
        quarter,
        year
    ]
    sql: ${TABLE}."session_user":"_datalakeMetadata":"received"::timestamp ;;
  }
    
  dimension: stream_id {
    description: "Stream Id"
    type: string
    sql: ${TABLE}."session_user":"_datalakeMetadata":"streamId"::string ;;
	group_label:"_datalakeMetadata"
  }
    
  dimension: ip {
    description: "Ip"
    type: string
    sql: ${TABLE}."session_user":"ip"::string ;;
  }
    
  dimension: agent {
    description: "Agent"
    type: string
    sql: ${TABLE}."session_user":"user_agent"::string ;;
  }
    
  dimension: id {
    description: "Id"
    type: string
    sql: ${TABLE}."session_user":"_datalakeMetadata":"id"::string ;;
	group_label:"_datalakeMetadata"
  }
    
  dimension: device {
    description: "Device"
    type: string
    sql: ${TABLE}."session_user":"details":"device"::string ;;
	group_label:"details"
  }
    
  dimension: log_id {
    description: "Id"
    type: string
    sql: ${TABLE}."session_user":"log_id"::string ;;
  }
    
  dimension: scope {
    description: "Scope"
    type: string
    sql: ${TABLE}."session_user":"details":"scope"::string ;;
	group_label:"details"
  }
    
  dimension: user_id {
    description: "Id"
    type: string
    sql: ${TABLE}."session_user":"user_id"::string ;;
  }
    
  dimension: type {
    description: "Type"
    type: string
    sql: ${TABLE}."session_user":"type"::string ;;
  }
    
  dimension: user_name {
    description: "Name"
    type: string
    sql: ${TABLE}."session_user":"user_name"::string ;;
  }
    
  dimension: client_version {
    description: "Client Version"
    type: string
    sql: ${TABLE}."session_user":"auth0_client":"version"::string ;;
	group_label:"auth0_client"
  }
    
  dimension: client_id {
    description: "Id"
    type: string
    sql: ${TABLE}."session_user":"client_id"::string ;;
  }
    
  dimension: target {
    description: "Target"
    type: string
    sql: ${TABLE}."session_user":"details":"target"::string ;;
	group_label:"details"
  }
    
  dimension_group: date {
    description: "Date"
    type: time
    timeframes: [
        raw,
        time,
        date,
        week,
        month,
        quarter,
        year
    ]
    sql: ${TABLE}."session_user":"date"::timestamp ;;
  }
    
  dimension: is_mobile {
    description: "Is Mobile"
    type: yesno
    sql: ${TABLE}."session_user":"isMobile"::boolean ;;
  }
    
  dimension: principal {
    description: "Principal"
    type: string
    sql: ${TABLE}."session_user":"_datalakeMetadata":"principal"::string ;;
	group_label:"_datalakeMetadata"
  }
    
  dimension: grant_type {
    description: "Grant Type"
    type: string
    sql: ${TABLE}."session_user":"details":"grant_type"::string ;;
	group_label:"details"
  }
    
  dimension: hostname {
    description: "Hostname"
    type: string
    sql: ${TABLE}."session_user":"hostname"::string ;;
  }
    
  dimension: client_name {
    description: "Client Name"
    type: string
    sql: ${TABLE}."session_user":"auth0_client":"name"::string ;;
	group_label:"auth0_client"
  }
    
  dimension: connection_id {
    description: "Id"
    type: string
    sql: ${TABLE}."session_user":"connection_id"::string ;;
  }
    
  dimension: api_type {
    description: "Api Type"
    type: string
    sql: ${TABLE}."session_user":"details":"api_type"::string ;;
	group_label:"details"
  }
    
  dimension: name {
    description: "Name"
    type: string
    sql: ${TABLE}."session_user":"client_name"::string ;;
  }
    
  dimension: _id {
    description: "Id"
    type: string
    sql: ${TABLE}."session_user":"_id"::string ;;
  }
    
}

view: description { 

  dimension: value {
    description: "Value"
    type: string
    sql: ${TABLE}.VALUE::string ;;
  }
    
}
