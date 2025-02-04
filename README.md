# Lambda para Insertar Películas en DynamoDB

## Descripción
Esta AWS Lambda recibe una lista de películas a través de un evento y las almacena en una tabla de **DynamoDB** llamada `Peliculas_S3D2_xideral`.  
Utiliza **Boto3** para interactuar con DynamoDB y `batch_writer()` para insertar múltiples registros de manera eficiente.

---

## Funcionamiento

1. **Recibe un evento con una lista de películas** en formato JSON.
2. **Valida los datos**:
   - Verifica que `peliculas` sea una lista.
   - Se asegura de que cada película sea un diccionario con el campo obligatorio `pelicula_id`.
3. **Convierte los valores numéricos a `str`** antes de insertarlos en DynamoDB (ya que DynamoDB no admite `int` o `float` directamente).
4. **Usa `batch_writer()` para inserción eficiente** de múltiples registros.
5. **Maneja errores con `try-except`**, capturando fallos en la conexión o estructura de datos.

---
