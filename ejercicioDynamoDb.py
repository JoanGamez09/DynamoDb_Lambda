import json
import boto3
from decimal import Decimal
from botocore.exceptions import BotoCoreError, ClientError

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = "Peliculas_S3D2_xideral"

def lambda_handler(event, context):
    table = dynamodb.Table(TABLE_NAME)

    try:
        peliculas = event.get("peliculas")

        # Validar si se recibieron datos y si es una lista
        if not isinstance(peliculas, list) or not peliculas:
            return {
                "statusCode": 400,
                "body": json.dumps("Error: Se esperaba una lista de peliculas.")
            }
        
        # Validar estructura de cada película
        for pelicula in peliculas:
            if not isinstance(pelicula, dict) or "pelicula_id" not in pelicula:
                return {
                    "statusCode": 400,
                    "body": json.dumps(f"Error: Formato incorrecto en la pelicula {pelicula}")
                }

        with table.batch_writer() as batch:
            for pelicula in peliculas:
                for key, value in pelicula.items():
                    if isinstance(value, (int, float)):
                        pelicula[key] = str(value)
            
                batch.put_item(Item=pelicula)

        return {
            "statusCode": 200,
            "body": json.dumps("Peliculas insertadas correctamente en DynamoDB")
        }

    except (BotoCoreError, ClientError) as db_error:
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error de DynamoDB: {str(db_error)}")
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error inesperado: {str(e)}")
        }