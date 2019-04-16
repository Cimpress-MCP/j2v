[![PyPI version](https://badge.fury.io/py/j2v.svg)](https://badge.fury.io/py/j2v)
# JSONs to Looker views (J2V)

J2V is a simple command-line tool to convert JSON to [Looker](https://looker.com/) readable files in forms of [Looker Views](https://docs.looker.com/reference/view-params/view) and [Looker Explores](https://docs.looker.com/reference/explore-params/explore).

Also it outputs an SQL with proper paths and explosion expressions.

This is useful to be used in combination with databases that are focusing on schema-on-read, and data is stored in raw JSON instead of exploded into columns of a table or view.

## Example use case

You have a table in your database. This table contains a column containing JSONs (one JSON per row). You are very curious how these data look like exploded, but you do not want to spend 2h going through the JSON structure and specifying all the fields just to surface them in Looker.

With J2V all the structures are discovered automatically and two files are generated - a Looker View and Looker Explore. All you need to do is copy/paste the output of this command line tool into your Looker project and you can start exploring.

# Usage

## Requirements

[Python 3](https://www.python.org/downloads/) must be installed.

## How to run
* use code from github or
* `pip install j2v`

## Parameters

* `json_files`: Files in JSON format, representing the data stored in a table
* `output_view`: Name of Looker View output file to be created
* `output_explore`: Name of Looker model output file to be created
* `sql_table_name`: Name of the DB table to be used (this is only used in the LookML files; no actual connection to a database will be done as part of this tool)
* `columnn_name`: Name of the column in the DB table as specified in `sql_table_name`. (this is only used in the LookML files; no actual connection to a database will be done as part of this tool)

## Output

* `output_view`: File containing definitions of Looker views (see [examples](./examples/) directory in this repository)
* `output_explore`: File containing definition of looker explore exploding the structures (see [examples](./examples/) directory in this repository)

## Example usage

### Using all parameters

`python3 main.py --json_files data1.json data2.json --output_view restaurant_chain.view --output_explore restaurant_chain.lkml --columnn_name raw_data --sql_table_name chains`

### Using only mandatory parameters

`python3 main.py --json_files order_example.json order_example2.json order_example3.json`<br />

# Contribution

## Project structure:

* `j2v` - source code of a package
* `examples` - working examples
* `tests` - tests

## Contribute

1. If unsure, open an issue for a discussion
1. Create a fork
1. Make your change
1. Make a pull request
1. Happy contribution!

## EXAMPLE

### Input: 
```json
{
  "apiVersion": "v3.4",
  "data Provider": "Eat me",
  "restaurants": [
    {
      "name": "Super Burger",
      "city": "Sydney",
      "country": "Australia",
      "address": "Big Street 3",
      "currency": "AUD",
      "menu": [
        {
          "dishName": "BurgerPlus",
          "price": 10,
          "indegrients": [
            "Meat",
            "Cheese",
            "Bun"
          ]
        }
      ]
    }
  ],
  "headquater": {
    "employees": 36,
    "city": "Olsztyn",
    "country": "Poland",
    "building": {
      "address": "3 Maja 10",
      "floors": [
        1,
        2,
        7
      ]
    }
  },
  "dataGenerationTimestamp": "2019-03-30T11:30:00.812Z",
  "payloadPrimaryKeyValue": "3ab21b54-22d6-473c-b055-4430f8927d4c"
}
```

### Ouput:

#### SQL output (now only Snowflake dialect supported):

```SQL

SELECT

---chains_table Information
chains_table."raw_data_column":"apiVersion"::string AS APIVERSION
,chains_table."raw_data_column":"data Provider"::string AS DATA_PROVIDER
,chains_table."raw_data_column":"dataGenerationTimestamp"::string AS DATAGENERATIONTIMESTAMP
,chains_table."raw_data_column":"headquater":"building":"address"::string AS HEADQUATER_BUILDING_ADDRESS
,chains_table."raw_data_column":"headquater":"city"::string AS HEADQUATER_CITY
,chains_table."raw_data_column":"headquater":"country"::string AS HEADQUATER_COUNTRY
,chains_table."raw_data_column":"headquater":"employees"::number AS HEADQUATER_EMPLOYEES
,chains_table."raw_data_column":"payloadPrimaryKeyValue"::string AS PAYLOADPRIMARYKEYVALUE
,
---restaurants Information
restaurants.VALUE:"address"::string AS RESTAURANTS_ADDRESS
,restaurants.VALUE:"city"::string AS RESTAURANTS_CITY
,restaurants.VALUE:"country"::string AS RESTAURANTS_COUNTRY
,restaurants.VALUE:"currency"::string AS RESTAURANTS_CURRENCY
,restaurants.VALUE:"name"::string AS RESTAURANTS_NAME
,
---restaurants_menu Information
restaurants_menu.VALUE:"dishName"::string AS RESTAURANTS_MENU_DISHNAME
,restaurants_menu.VALUE:"price"::number AS RESTAURANTS_MENU_PRICE
,
---restaurants_menu_indegrients Information
restaurants_menu_indegrients.VALUE::string AS RESTAURANTS_MENU_INDEGRIENTS_VALUE
,
---headquater_building_floors Information
headquater_building_floors.VALUE::number AS HEADQUATER_BUILDING_FLOORS_VALUE
FROM chains_table,
LATERAL FLATTEN(OUTER => TRUE, INPUT => chains_table."raw_data_column":"restaurants") restaurants
,LATERAL FLATTEN(OUTER => TRUE, INPUT => restaurants.VALUE:"menu") restaurants_menu
,LATERAL FLATTEN(OUTER => TRUE, INPUT => restaurants_menu.VALUE:"indegrients") restaurants_menu_indegrients
,LATERAL FLATTEN(OUTER => TRUE, INPUT => chains_table."raw_data_column":"headquater":"building":"floors") headquater_building_floors


```

#### Ouput files:

##### View file:

```LookML



view: chains_table { 
  sql_table_name: chains_table ;;

  dimension: city {
    description: "City"
    type: string
    sql: ${TABLE}."raw_data_column":"headquater":"city"::string ;;
  }
    
  dimension: provider {
    description: "Provider"
    type: string
    sql: ${TABLE}."raw_data_column":"data Provider"::string ;;
  }
    
  dimension: building_address {
    description: "Building Address"
    type: string
    sql: ${TABLE}."raw_data_column":"headquater":"building":"address"::string ;;
  }
    
  dimension: payload_primary_key_value {
    description: "Payload Primary Key Value"
    type: string
    sql: ${TABLE}."raw_data_column":"payloadPrimaryKeyValue"::string ;;
  }
    
  dimension: data_generation_timestamp {
    description: "Data Generation Timestamp"
    type: date_time
    sql: ${TABLE}."raw_data_column":"dataGenerationTimestamp"::string ;;
  }
    
  dimension: api_version {
    description: "Api Version"
    type: string
    sql: ${TABLE}."raw_data_column":"apiVersion"::string ;;
  }
    
  dimension: employees {
    description: "Employees"
    type: number
    sql: ${TABLE}."raw_data_column":"headquater":"employees"::number ;;
  }
    
  dimension: country {
    description: "Country"
    type: string
    sql: ${TABLE}."raw_data_column":"headquater":"country"::string ;;
  }
    
}

view: restaurants { 

  dimension: country {
    description: "Country"
    type: string
    sql: ${TABLE}.VALUE:"country"::string ;;
  }
    
  dimension: address {
    description: "Address"
    type: string
    sql: ${TABLE}.VALUE:"address"::string ;;
  }
    
  dimension: currency {
    description: "Currency"
    type: string
    sql: ${TABLE}.VALUE:"currency"::string ;;
  }
    
  dimension: name {
    description: "Name"
    type: string
    sql: ${TABLE}.VALUE:"name"::string ;;
  }
    
  dimension: city {
    description: "City"
    type: string
    sql: ${TABLE}.VALUE:"city"::string ;;
  }
    
}

view: restaurants_menu { 

  dimension: menu_price {
    description: "Menu Price"
    type: number
    sql: ${TABLE}.VALUE:"price"::number ;;
  }
    
  dimension: menu_dish_name {
    description: "Menu Dish Name"
    type: string
    sql: ${TABLE}.VALUE:"dishName"::string ;;
  }
    
}

view: restaurants_menu_indegrients { 

  dimension: menu_indegrients_value {
    description: "Menu Indegrients Value"
    type: string
    sql: ${TABLE}.VALUE::string ;;
  }
    
}

view: headquater_building_floors { 

  dimension: building_floors_value {
    description: "Building Floors Value"
    type: number
    sql: ${TABLE}.VALUE::number ;;
  }
    
}


```

##### Explore file:

```LookML
include: "restaurant_chain.view"
   
explore: chains_table {
  view_name: chains_table
  from: chains_table
  label: "chains_table explore"
  description: "chains_table explore"

  join: restaurants {
     from: restaurants
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => chains_table."raw_data_column":"restaurants") restaurants;;
     relationship: one_to_many 
  }
  
  join: restaurants_menu {
     from: restaurants_menu
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => restaurants.VALUE:"menu") restaurants_menu;;
     relationship: one_to_many 
     required_joins: [restaurants]
  }
  
  join: restaurants_menu_indegrients {
     from: restaurants_menu_indegrients
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => restaurants_menu.VALUE:"indegrients") restaurants_menu_indegrients;;
     relationship: one_to_many 
     required_joins: [restaurants_menu]
  }
  
  join: headquater_building_floors {
     from: headquater_building_floors
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => chains_table."raw_data_column":"headquater":"building":"floors") headquater_building_floors;;
     relationship: one_to_many 
  }
  
}

```


