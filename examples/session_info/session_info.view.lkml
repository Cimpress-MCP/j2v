
view: JSON_TABLE { 
  sql_table_name: session_info ;;

  dimension: ocsp_mode {
    description: "Ocsp Mode"
    type: string
    sql: ${TABLE}."session_user":"clientEnvironment":"OCSP_MODE"::string ;;
	group_label:"clientEnvironment"
  }
    
  dimension: java_version {
    description: "Java Version"
    type: string
    sql: ${TABLE}."session_user":"clientEnvironment":"JAVA_VERSION"::string ;;
	group_label:"clientEnvironment"
  }
    
  dimension: current_database {
    description: "Current Database"
    type: string
    sql: ${TABLE}."session_user":"currentDatabase"::string ;;
  }
    
  dimension: os_version {
    description: "Os Version"
    type: string
    sql: ${TABLE}."session_user":"clientEnvironment":"OS_VERSION"::string ;;
	group_label:"clientEnvironment"
  }
    
  dimension: database_provider {
    description: "Database Provider"
    type: string
    sql: ${TABLE}."session_user":"databaseProvider"::string ;;
  }
    
  dimension: current_warehouse {
    description: "Current Warehouse"
    type: string
    sql: ${TABLE}."session_user":"currentWarehouse"::string ;;
  }
    
  dimension: client_application {
    description: "Client Application"
    type: string
    sql: ${TABLE}."session_user":"clientApplication"::string ;;
  }
    
  dimension: java_runtime {
    description: "Java Runtime"
    type: string
    sql: ${TABLE}."session_user":"clientEnvironment":"JAVA_RUNTIME"::string ;;
	group_label:"clientEnvironment"
  }
    
  dimension: java_vm {
    description: "Java Vm"
    type: string
    sql: ${TABLE}."session_user":"clientEnvironment":"JAVA_VM"::string ;;
	group_label:"clientEnvironment"
  }
    
  dimension: application {
    description: "Application"
    type: string
    sql: ${TABLE}."session_user":"clientEnvironment":"APPLICATION"::string ;;
	group_label:"clientEnvironment"
  }
    
  dimension: user_name {
    description: "User Name"
    type: string
    sql: ${TABLE}."session_user":"userName"::string ;;
  }
    
  dimension: client_net_address {
    description: "Client Net Address"
    type: string
    sql: ${TABLE}."session_user":"clientNetAddress"::string ;;
  }
    
  dimension: user_login_name {
    description: "User Login Name"
    type: string
    sql: ${TABLE}."session_user":"userLoginName"::string ;;
  }
    
  dimension: os {
    description: "Os"
    type: string
    sql: ${TABLE}."session_user":"clientEnvironment":"OS"::string ;;
	group_label:"clientEnvironment"
  }
    
  dimension: user_display_name {
    description: "User Display Name"
    type: string
    sql: ${TABLE}."session_user":"userDisplayName"::string ;;
  }
    
  dimension: is_active {
    description: "Is Active"
    type: yesno
    sql: ${TABLE}."session_user":"isActive"::boolean ;;
  }
    
  dimension: current_role {
    description: "Current Role"
    type: string
    sql: ${TABLE}."session_user":"currentRole"::string ;;
  }
    
  dimension: id {
    description: "Id"
    type: number
    sql: ${TABLE}."session_user":"id"::number ;;
  }
    
  dimension: current_schema {
    description: "Current Schema"
    type: string
    sql: ${TABLE}."session_user":"currentSchema"::string ;;
  }
    
  dimension: account_name {
    description: "Account Name"
    type: string
    sql: ${TABLE}."session_user":"accountName"::string ;;
  }
    
}
