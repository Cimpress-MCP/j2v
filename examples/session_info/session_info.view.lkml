
view: session { 
  sql_table_name: session_info ;;

  dimension: account_name {
    label: "Account name"
    description: "Account name"
    type: string
    sql: ${TABLE}."session_user":"accountName"::string ;;
  }
    
  dimension: application {
    label: "Application"
    description: "Application"
    type: string
    sql: ${TABLE}."session_user":"clientEnvironment":"APPLICATION"::string ;;
    group_label: "Client environment"
  }
    
  dimension: client_application {
    label: "Client application"
    description: "Client application"
    type: string
    sql: ${TABLE}."session_user":"clientApplication"::string ;;
  }
    
  dimension: client_net_address {
    label: "Client net address"
    description: "Client net address"
    type: string
    sql: ${TABLE}."session_user":"clientNetAddress"::string ;;
  }
    
  dimension: current_database {
    label: "Current database"
    description: "Current database"
    type: string
    sql: ${TABLE}."session_user":"currentDatabase"::string ;;
  }
    
  dimension: current_role {
    label: "Current role"
    description: "Current role"
    type: string
    sql: ${TABLE}."session_user":"currentRole"::string ;;
  }
    
  dimension: current_schema {
    label: "Current schema"
    description: "Current schema"
    type: string
    sql: ${TABLE}."session_user":"currentSchema"::string ;;
  }
    
  dimension: current_warehouse {
    label: "Current warehouse"
    description: "Current warehouse"
    type: string
    sql: ${TABLE}."session_user":"currentWarehouse"::string ;;
  }
    
  dimension: database_provider {
    label: "Database provider"
    description: "Database provider"
    type: string
    sql: ${TABLE}."session_user":"databaseProvider"::string ;;
  }
    
  dimension: id {
    label: "Id"
    description: "Id"
    primary_key: yes
    type: number
    sql: ${TABLE}."session_user":"id"::number ;;
  }
    
  dimension: is_active {
    label: "Is active"
    description: "Is active"
    type: yesno
    sql: ${TABLE}."session_user":"isActive"::boolean ;;
  }
    
  dimension: java_runtime {
    label: "Java runtime"
    description: "Java runtime"
    type: string
    sql: ${TABLE}."session_user":"clientEnvironment":"JAVA_RUNTIME"::string ;;
    group_label: "Client environment"
  }
    
  dimension: java_version {
    label: "Java version"
    description: "Java version"
    type: string
    sql: ${TABLE}."session_user":"clientEnvironment":"JAVA_VERSION"::string ;;
    group_label: "Client environment"
  }
    
  dimension: java_vm {
    label: "Java vm"
    description: "Java vm"
    type: string
    sql: ${TABLE}."session_user":"clientEnvironment":"JAVA_VM"::string ;;
    group_label: "Client environment"
  }
    
  dimension: ocsp_mode {
    label: "Ocsp mode"
    description: "Ocsp mode"
    type: string
    sql: ${TABLE}."session_user":"clientEnvironment":"OCSP_MODE"::string ;;
    group_label: "Client environment"
  }
    
  dimension: os {
    label: "Os"
    description: "Os"
    type: string
    sql: ${TABLE}."session_user":"clientEnvironment":"OS"::string ;;
    group_label: "Client environment"
  }
    
  dimension: os_version {
    label: "Os version"
    description: "Os version"
    type: string
    sql: ${TABLE}."session_user":"clientEnvironment":"OS_VERSION"::string ;;
    group_label: "Client environment"
  }
    
  dimension: secret_for_you_id {
    label: "Id"
    description: "Id"
    type: number
    sql: ${TABLE}."session_user":"ALL":"things":"secret":"secret_for_you":"id"::number ;;
    group_label: "Secret for you"
  }
    
  dimension: secret_id {
    label: "Id"
    description: "Id"
    type: number
    sql: ${TABLE}."session_user":"ALL":"things":"secret":"id"::number ;;
    group_label: "Secret"
  }
    
  dimension: things_id {
    label: "Id"
    description: "Id"
    type: number
    sql: ${TABLE}."session_user":"ALL":"things":"id"::number ;;
    group_label: "Things"
  }
    
  dimension: user_display_name {
    label: "User display name"
    description: "User display name"
    type: string
    sql: ${TABLE}."session_user":"userDisplayName"::string ;;
  }
    
  dimension: user_login_name {
    label: "User login name"
    description: "User login name"
    type: string
    sql: ${TABLE}."session_user":"userLoginName"::string ;;
  }
    
  dimension: user_name {
    label: "User name"
    description: "User name"
    type: string
    sql: ${TABLE}."session_user":"userName"::string ;;
  }
    
}
