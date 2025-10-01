from mypy_boto3_dynamodb.type_defs import (
    ScanInputTableScanTypeDef,
    GetItemInputTableGetItemTypeDef,
    PutItemInputTablePutItemTypeDef,
    UpdateItemInputTableUpdateItemTypeDef,
    QueryInputTableQueryTypeDef,
    TableAttributeValueTypeDef,
    DeleteItemInputTableDeleteItemTypeDef,
)
from typing import Any, Dict
import boto3
from botocore.exceptions import ClientError


class DynamodbService:
    def __init__(self, table_name):
        self.ddb_resource = boto3.resource("dynamodb")
        self.Table = self.ddb_resource.Table(table_name)

    @staticmethod
    def _enhance_request(
        request: dict[str, any], default: dict[str, any] = dict()
    ) -> dict[str, Any]:
        return default | request

    def get(self, request: GetItemInputTableGetItemTypeDef) -> dict:
        get_request = self._enhance_request(request, {"ReturnConsumedCapacity": "NONE"})
        try:
            response: dict = self.Table.get_item(**get_request)
        except ClientError as err:
            raise
        else:
            return response.get("Item", {})

    def put(
        self, request: PutItemInputTablePutItemTypeDef
    ) -> Dict[str, TableAttributeValueTypeDef]:
        response: dict = self.Table.put_item(**request)

        return response.get("ResponseMetadata", None)

    def update(
        self, request: UpdateItemInputTableUpdateItemTypeDef
    ) -> Dict[str, TableAttributeValueTypeDef]:
        response: dict = self.Table.update_item(**request)
        return response.get("ResponseMetadata", None)

    def query(
        self, request: QueryInputTableQueryTypeDef
    ) -> Dict[str, TableAttributeValueTypeDef]:
        response: dict = self.Table.query(**request)
        return {
            "items": response.get("Items", []),
            "lastEvaluatedKey": response.get("LastEvaluatedKey", None),
        }

    def scan(
        self, request: ScanInputTableScanTypeDef
    ) -> Dict[str, TableAttributeValueTypeDef]:
        response: dict = self.Table.scan(**request)
        return {
            "items": response.get("Items", []),
            "lastEvaluatedKey": response.get("LastEvaluatedKey", None),
        }

    def delete(
        self, request: DeleteItemInputTableDeleteItemTypeDef
    ) -> Dict[str, TableAttributeValueTypeDef]:
        response: dict = self.Table.delete_item(**request)
        return response
