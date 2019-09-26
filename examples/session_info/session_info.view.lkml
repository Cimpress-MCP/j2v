
view: JSON_TABLE { 
  sql_table_name: session_info ;;

  dimension: vm {
    description: "Vm"
    type: string
    sql: ${TABLE}."session_user":"JAVA_VM"::string ;;
  }
    
  dimension: version {
    description: "Version"
    type: string
    sql: ${TABLE}."session_user":"JAVA_VERSION"::string ;;
  }
    
  dimension: current_database {
    description: "Current Database"
    type: string
    sql: ${TABLE}."session_user":"currentDatabase"::string ;;
  }
    
  dimension: current_schema {
    description: "Current Schema"
    type: string
    sql: ${TABLE}."session_user":"currentSchema"::string ;;
  }
    
  dimension: user_name {
    description: "User Name"
    type: string
    sql: ${TABLE}."session_user":"userName"::string ;;
  }
    
  dimension: client_application {
    description: "Client Application"
    type: string
    sql: ${TABLE}."session_user":"clientApplication"::string ;;
  }
    
  dimension: runtime {
    description: "Runtime"
    type: string
    sql: ${TABLE}."session_user":"JAVA_RUNTIME"::string ;;
  }
    
  dimension: version_id {
    description: "Version Id"
    type: string
    sql: ${TABLE}."session_user":"OS_VERSION":"id"::string ;;
	group_label:"OS_VERSION"
  }
    
  dimension: version_name {
    description: "Version Name"
    type: string
    sql: ${TABLE}."session_user":"OS_VERSION":"name"::string ;;
	group_label:"OS_VERSION"
  }
    
  dimension: _id {
    description: "Id"
    type: number
    sql: ${TABLE}."session_user":"id"::number ;;
  }
    
  dimension: current_warehouse {
    description: "Current Warehouse"
    type: string
    sql: ${TABLE}."session_user":"currentWarehouse"::string ;;
  }
    
  dimension: user_display_name {
    description: "User Display Name"
    type: string
    sql: ${TABLE}."session_user":"userDisplayName"::string ;;
  }
    
  dimension: mode {
    description: "Mode"
    type: string
    sql: ${TABLE}."session_user":"OCSP_MODE"::string ;;
  }
    
  dimension: database_provider {
    description: "Database Provider"
    type: string
    sql: ${TABLE}."session_user":"databaseProvider"::string ;;
  }
    
  dimension: id {
    description: "Id"
    type: number
    sql: ${TABLE}."session_user":"clientEnvironment":"id"::number ;;
	group_label:"clientEnvironment"
  }
    
  dimension: name {
    description: "Name"
    type: string
    sql: ${TABLE}."session_user":"clientEnvironment":"name"::string ;;
	group_label:"clientEnvironment"
  }
    
  dimension: os {
    description: "Os"
    type: string
    sql: ${TABLE}."session_user":"OS"::string ;;
  }
    
  dimension: current_role {
    description: "Current Role"
    type: string
    sql: ${TABLE}."session_user":"currentRole"::string ;;
  }
    
  dimension: application {
    description: "Application"
    type: string
    sql: ${TABLE}."session_user":"APPLICATION"::string ;;
  }
    
  dimension: is_active {
    description: "Is Active"
    type: yesno
    sql: ${TABLE}."session_user":"isActive"::boolean ;;
  }
    
  dimension: account_name {
    description: "Account Name"
    type: string
    sql: ${TABLE}."session_user":"accountName"::string ;;
  }
    
  dimension: user_login_name {
    description: "User Login Name"
    type: string
    sql: ${TABLE}."session_user":"userLoginName"::string ;;
  }
    
  dimension: client_net_address {
    description: "Client Net Address"
    type: string
    sql: ${TABLE}."session_user":"clientNetAddress"::string ;;
  }
    
}
