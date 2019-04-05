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

#### SQL output:

```SQL
SELECT

---chains_table Information
chains_table.raw_data_column:"data Provider"::string
,chains_table.raw_data_column:apiVersion::string
,chains_table.raw_data_column:dataGenerationTimestamp::string
,chains_table.raw_data_column:headquater:building:address::string
,chains_table.raw_data_column:headquater:city::string
,chains_table.raw_data_column:headquater:country::string
,chains_table.raw_data_column:headquater:employees::number
,chains_table.raw_data_column:payloadPrimaryKeyValue::string
,
---restaurants Information
restaurants.VALUE:address::string
,restaurants.VALUE:city::string
,restaurants.VALUE:country::string
,restaurants.VALUE:currency::string
,restaurants.VALUE:name::string
,
---menu Information
menu.VALUE:dishName::string
,menu.VALUE:price::number
,
---indegrients Information
indegrients.VALUE::string
,
---floors Information
floors.VALUE::number
FROM chains_table,
LATERAL FLATTEN(OUTER => TRUE, INPUT => chains_table.raw_data_column:restaurants) restaurants
,LATERAL FLATTEN(OUTER => TRUE, INPUT => restaurants.VALUE:menu) menu
,LATERAL FLATTEN(OUTER => TRUE, INPUT => menu.VALUE:indegrients) indegrients
,LATERAL FLATTEN(OUTER => TRUE, INPUT => chains_table.raw_data_column:headquater:building:floors) floors
```

#### Ouput files:

##### View file:

```LookML

view: chains_table { 
  sql_table_name: chains_table ;;

  dimension: building_address {
    description: "Building Address"
    type: string
    sql: ${TABLE}.raw_data_column:headquater:building:address::string ;;
  }
    
  dimension: headquater_city {
    description: "Headquater City"
    type: string
    sql: ${TABLE}.raw_data_column:headquater:city::string ;;
  }
    
  dimension: raw_data_column_api_version {
    description: "Raw data column Api Version"
    type: string
    sql: ${TABLE}.raw_data_column:apiVersion::string ;;
  }
    
  dimension: headquater_country {
    description: "Headquater Country"
    type: string
    sql: ${TABLE}.raw_data_column:headquater:country::string ;;
  }
    
  dimension: headquater_employees {
    description: "Headquater Employees"
    type: number
    sql: ${TABLE}.raw_data_column:headquater:employees::number ;;
  }
    
  dimension: raw_data_column_data_generation_timestamp {
    description: "Raw data column Data Generation Timestamp"
    type: date_time
    sql: ${TABLE}.raw_data_column:dataGenerationTimestamp::string ;;
  }
    
  dimension: raw_data_column_data__provider {
    description: "Raw data column Data  Provider"
    type: string
    sql: ${TABLE}.raw_data_column:"data Provider"::string ;;
  }
    
  dimension: raw_data_column_payload_primary_key_value {
    description: "Raw data column Payload Primary Key Value"
    type: string
    sql: ${TABLE}.raw_data_column:payloadPrimaryKeyValue::string ;;
  }
    
}

view: restaurants { 

  dimension: address {
    description: "Address"
    type: string
    sql: ${TABLE}.VALUE:address::string ;;
  }
    
  dimension: city {
    description: "City"
    type: string
    sql: ${TABLE}.VALUE:city::string ;;
  }
    
  dimension: name {
    description: "Name"
    type: string
    sql: ${TABLE}.VALUE:name::string ;;
  }
    
  dimension: country {
    description: "Country"
    type: string
    sql: ${TABLE}.VALUE:country::string ;;
  }
    
  dimension: currency {
    description: "Currency"
    type: string
    sql: ${TABLE}.VALUE:currency::string ;;
  }
    
}

view: menu { 

  dimension: price {
    description: "Price"
    type: number
    sql: ${TABLE}.VALUE:price::number ;;
  }
    
  dimension: dish_name {
    description: "Dish Name"
    type: string
    sql: ${TABLE}.VALUE:dishName::string ;;
  }
    
}

view: indegrients { 

  dimension: _value {
    description: " Value"
    type: string
    sql: ${TABLE}.VALUE::string ;;
  }
    
}

view: floors { 

  dimension: _value {
    description: " Value"
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
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => chains_table.raw_data_column:restaurants) restaurants;;
     relationship: one_to_many 
  }
  
  join: menu {
     from: menu
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => restaurants.VALUE:menu) menu;;
     relationship: one_to_many 
     required_joins: [restaurants]
  }
  
  join: indegrients {
     from: indegrients
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => menu.VALUE:indegrients) indegrients;;
     relationship: one_to_many 
     required_joins: [menu]
  }
  
  join: floors {
     from: floors
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => chains_table.raw_data_column:headquater:building:floors) floors;;
     relationship: one_to_many 
  }
  
}
```


