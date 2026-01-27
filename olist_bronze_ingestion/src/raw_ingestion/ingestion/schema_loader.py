import json
from pyspark.sql.types import StructType, StructField
from pyspark.sql.types import StringType, DecimalType, IntegerType,TimestampType

Type_Mapping = {
    "string": StringType(),
    "int":IntegerType(),
    "decimal":DecimalType(),
    "timestamp":TimestampType()
}

def load_schema(spark,schemaPath:str,enforce_strict: bool) -> StructType:
    with open(schemaPath) as f:
        schema = json.load(f)
    fields = []
    for field in schema["columns"]:
        fields.append(StructField(field["name"]),Type_Mapping[field["type"]],field.get("nullable",True))
    return StructType(fields)
