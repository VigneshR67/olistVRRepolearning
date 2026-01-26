#environment configs
#rejection rules - are set at json level
#email configs ( will also need to check if we can set this at the task level)

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ColumnConfig:
    name: str
    type: str
    nullable: bool = True


@dataclass
class SchemaConfig:
    schema_file: str
    allow_extra_columns: bool = True
    enforce_nullable: bool = True


@dataclass
class IngestionRulesConfig:
    reject_empty_files: bool = True
    reject_threshold_percent: float = 0.0
    allow_duplicate_files: bool = False

    def __post_init__(self):
        if not 0 <= self.reject_threshold_percent <= 100:
            raise ValueError(
                "reject_threshold_percent must be between 0 and 100"
            )
        


@dataclass
class FilePatternConfig:
    regex: str
    date_from_filename: bool = False

    #Example of derived field
    compiled_regex: re.Pattern = field(init=False) #this is will not expect the value at runtime from config

    def __post_init__(self):
        self.compiled_regex = re.compile(self.regex)

        #at runtime
        #config.file_pattern.compiled_regex.match(filename)


@dataclass
class ReadOptionsConfig:
    header: bool = True
    delimiter: str = ","
    mode: str = "PERMISSIVE" #need to read more on mode ( how to pass)
    #dynamically to these variables. DROPMALFORMED, FAIL_FAST

#these are default properties
@dataclass
class SparkProperties:
    spark_sql_shuffle_partitions: str = "200"
    spark_sql_adaptive_enabled: str = "true"
    spark_sql_adaptive_coalesce: str ="true"
    spark_delta_optimize_write: str ="true"


@dataclass
class SourceConfig:
    source_name: str
    zipped:bool
    bucket_name: str
    landing_path: str
    raw_table: str
    file_format: str

    schema: SchemaConfig
    ingestion_rules: IngestionRulesConfig
    file_pattern: FilePatternConfig
    read_options: ReadOptionsConfig
    spark_config: SparkProperties

    #this is just to validate configs, because there is possibility to mess up the source json
    def __post_init__(self):
        if not self.landing_path:
            raise ValueError("landing_path cannot be empty")
        if self.file_format == "csv" and not self.read_options.header:
            raise ValueError("CSV files must have header")



import json

#this is where the source congfig is loaded and would be called from the orchestrator
def load_source_config(path: str) -> SourceConfig:
    with open(path) as f:
        data = json.load(f)

    return SourceConfig(
        source_name=data["source_name"],
        zipped=data["zipped"],
        bucket_name=data["bucketname"],
        landing_path=data["landing_path"],
        raw_table=data["raw_table"],
        file_format=data["file_format"],
        schema=SchemaConfig(**data.get("schema", {})),
        ingestion_rules=IngestionRulesConfig(**data.get("ingestion_rules", {})),
        file_pattern=FilePatternConfig(**data.get("file_pattern", {})),
        read_options=ReadOptionsConfig(**data.get("read_options", {})),
        spark_config=SparkProperties(**data.get("spark_properties", {}))
    )
