# mysql_operations.py
import mysql.connector
import numpy as np
import cv2
import os

mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'jay@gajanan123',
    'database': 'liveness_detection'
}


# def fetch_employee_image(EmpCode, mysql_config):
#     try:
#         connection = mysql.connector.connect(**mysql_config)
#         cursor = connection.cursor()

#         query = "SELECT img FROM employees WHERE EmpCode = %s"
#         cursor.execute(query, (EmpCode,))
#         result = cursor.fetchone()
#         print(result)
#         if result:
#             # Extract image bytes and decode
#             image_bytes = result[0]
#             decoded_image = cv2.imdecode(np.frombuffer(image_bytes, dtype=np.uint8), 1)
#             print("Image fetched from MySQL database")
#             return decoded_image

#     except Exception as e:
#         print(f"Error fetching image from MySQL database: {e}")

#     finally:
#         # Close the database connection
#         cursor.close()
#         connection.close()

#     print("Image not fetched from MySQL database or error occurred.")
#     return None



def fetch_employee_image(EmpCode, mysql_config):
    try:
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        query = "SELECT img FROM employees WHERE EmpCode = %s"
        cursor.execute(query, (EmpCode,))
        
        
        result = cursor.fetchone()
        

        if result:
            # Extract and decode image bytes
            image_bytes = result[0]
            # decoded_image = cv2.imdecode(np.frombuffer(image_bytes, dtype=np.uint8), 1)
            # print("Image fetched from MySQL database")

            # Assuming the image path is stored in bytes, decode it
            image_path = image_bytes.decode('utf-8')
            # Ensure correct path format (replace 'C:Users' with 'C:\\Users')
            image_path = image_path.replace('C:Users', 'C:\\Users')
            image_path = str(image_path.replace("\\", "\\\\"))
            # image_path=os.startfile(image_path)
            # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",image_path)
            # print("Image path in the database:", image_path)
            # # return image_path
            # Check if the file exists
            # Read the image
            
            image = cv2.imread(image_path)
            print("fetch function return image : ",image.shape)
            # cv2.imshow("image_window",image_path)

            # # If needed, convert the image to grayscale
            # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # # Encode the image to bytes
            # encoded_image = cv2.imencode(".jpg", gray_image)

            # # Decode the image
            # decoded_image = cv2.imdecode(encoded_image, 1)
            # decoded_image = cv2.imdecode(np.frombuffer(image_bytes, dtype=np.uint8), 1)
            # if os.path.isfile(image_path):
            return image
            # else:
            #     print("Image file not found.")
            #     return None

    except Exception as e:
        print(f"Error fetching image from MySQL database: {e}")

    finally:
        # Close the database connection
        cursor.close()
        connection.close()

    # print("Image not fetched from MySQL database or error occurred.")
    # return None



    
# Function to get employee name from the MySQL database
def get_employee_name(EmpCode, mysql_config):
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()

    query = "SELECT FirstName, LastName FROM employees WHERE EmpCode = %s"
    cursor.execute(query, (EmpCode,))
    result = cursor.fetchone()
    result=" ".join(list(result))
 
    print("first and last name of employee @@@@@@@@@@@@@@@@@@@@@@@@",result)
    if result:
        return result

    return None


if __name__=="__main__":
    EmpCode="PN06"
    mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'jay@gajanan123',
    'database': 'liveness_detection'
} 
    get_employee_name(EmpCode, mysql_config)
  
    employee_image = fetch_employee_image(EmpCode, mysql_config)

    if employee_image is not None:
        # Now, 'employee_image' contains the image data as a NumPy array
        # Display the image using OpenCV
        cv2.imshow("Employee Image", employee_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Image not fetched or an error occurred.")
