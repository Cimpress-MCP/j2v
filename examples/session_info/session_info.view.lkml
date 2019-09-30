
view: session { 
  sql_table_name: session_info ;;

  dimension: account_name {
    description: "Account Name"
    type: string
    sql: ${TABLE}."session_user":"accountName"::string ;;
  }
    
  dimension: application {
    description: "Application"
    type: string
    sql: ${TABLE}."session_user":"clientEnvironment":"APPLICATION"::string ;;
    group_label:"clientEnvironment"
  }
    
  dimension: client_application {
    description: "Client Application"
    type: string
    sql: ${TABLE}."session_user":"clientApplication"::string ;;
  }
    
  dimension: client_net_address {
    description: "Client Net Address"
    type: string
    sql: ${TABLE}."session_user":"clientNetAddress"::string ;;
  }
    
  dimension: current_database {
    description: "Current Database"
    type: string
    sql: ${TABLE}."session_user":"currentDatabase"::string ;;
  }
    
  dimension: current_role {
    description: "Current Role"
    type: string
    sql: ${TABLE}."session_user":"currentRole"::string ;;
  }
    
  dimension: current_schema {
    description: "Current Schema"
    type: string
    sql: ${TABLE}."session_user":"currentSchema"::string ;;
  }
    
  dimension: current_warehouse {
    description: "Current Warehouse"
    type: string
    sql: ${TABLE}."session_user":"currentWarehouse"::string ;;
  }
    
  dimension: database_provider {
    description: "Database Provider"
    type: string
    sql: ${TABLE}."session_user":"databaseProvider"::string ;;
  }
    
  dimension: id {
    description: "Id"
    type: number
    sql: ${TABLE}."session_user":"id"::number ;;
  }
    
  dimension: is_active {
    description: "Is Active"
    type: yesno
    sql: ${TABLE}."session_user":"isActive"::boolean ;;
  }
    
  dimension: java_runtime {
    description: "Java Runtime"
    type: string
    sql: ${TABLE}."session_user":"clientEnvironment":"JAVA_RUNTIME"::string ;;
    group_label:"clientEnvironment"
  }
    
  dimension: java_version {
    description: "Java Version"
    type: string
    sql: ${TABLE}."session_user":"clientEnvironment":"JAVA_VERSION"::string ;;
    group_label:"clientEnvironment"
  }
    
  dimension: java_vm {
    description: "Java Vm"
    type: string
    sql: ${TABLE}."session_user":"clientEnvironment":"JAVA_VM"::string ;;
    group_label:"clientEnvironment"
  }
    
  dimension: ocsp_mode {
    description: "Ocsp Mode"
    type: string
    sql: ${TABLE}."session_user":"clientEnvironment":"OCSP_MODE"::string ;;
    group_label:"clientEnvironment"
  }
    
  dimension: os {
    description: "Os"
    type: string
    sql: ${TABLE}."session_user":"clientEnvironment":"OS"::string ;;
    group_label:"clientEnvironment"
  }
    
  dimension: os_version {
    description: "Os Version"
    type: string
    sql: ${TABLE}."session_user":"clientEnvironment":"OS_VERSION"::string ;;
    group_label:"clientEnvironment"
  }
    
  dimension: things_id {
    description: "Things Id"
    type: number
    sql: ${TABLE}."session_user":"ALL":"things":"id"::number ;;
    group_label:"things"
  }
    
  dimension: things_secret_id {
    description: "Things Secret Id"
    type: number
    sql: ${TABLE}."session_user":"ALL":"things":"secret":"id"::number ;;
    group_label:"secret"
  }
    
  dimension: things_secret_secret_for_you_id {
    description: "Things Secret Secret For You Id"
    type: number
    sql: ${TABLE}."session_user":"ALL":"things":"secret":"secret_for_you":"id"::number ;;
    group_label:"secret_for_you"
  }
    
  dimension: user_display_name {
    description: "User Display Name"
    type: string
    sql: ${TABLE}."session_user":"userDisplayName"::string ;;
  }
    
  dimension: user_login_name {
    description: "User Login Name"
    type: string
    sql: ${TABLE}."session_user":"userLoginName"::string ;;
  }
    
  dimension: user_name {
    description: "User Name"
    type: string
    sql: ${TABLE}."session_user":"userName"::string ;;
  }
    
}
