# model breaking constraints
trino_model_char_value_to_int_column = """
{{
  config(
    materialized = "table"
  )
}}

select
  -- char value for 'id', which is integer type
  'char_value' as id,
  -- change the color as well (to test rollback)
  'red' as color,
  '2019-01-01' as date_day
"""

trino_model_schema_yml = """
version: 2
models:
  - name: my_model
    config:
      contract:
        enforced: true
    columns:
      - name: id
        quote: true
        data_type: integer
        description: hello
        constraints:
          - type: check
            expression: (id > 0)
        tests:
          - unique
      - name: color
        data_type: varchar
      - name: date_day
        data_type: varchar
  - name: my_model_error
    config:
      contract:
        enforced: true
    columns:
      - name: id
        data_type: integer
        description: hello
        constraints:
          - type: check
            expression: (id > 0)
        tests:
          - unique
      - name: color
        data_type: varchar
      - name: date_day
        data_type: varchar
  - name: my_model_wrong_order
    config:
      contract:
        enforced: true
    columns:
      - name: id
        data_type: integer
        description: hello
        constraints:
          - type: check
            expression: (id > 0)
        tests:
          - unique
      - name: color
        data_type: varchar
      - name: date_day
        data_type: varchar
  - name: my_model_wrong_name
    config:
      contract:
        enforced: true
    columns:
      - name: id
        data_type: integer
        description: hello
        constraints:
          - type: check
            expression: (id > 0)
        tests:
          - unique
      - name: color
        data_type: varchar
      - name: date_day
        data_type: varchar
"""

trino_constrained_model_schema_yml = """
version: 2
models:
  - name: my_model
    config:
      contract:
        enforced: true
    constraints:
      - type: check
        expression: (id > 0)
      - type: primary_key
        columns: [ id ]
      - type: unique
        columns: [ color, date_day ]
        name: strange_uniqueness_requirement
    columns:
      - name: id
        quote: true
        data_type: integer
        description: hello
        constraints:
          - type: not_null
        tests:
          - unique
      - name: color
        data_type: varchar
      - name: date_day
        data_type: varchar
"""
