# Introduction
This project highlights the potential of Industrial IoT (IIoT) through Azure IoT services. It serves as an educational initiative, offering a practical example of my approach to studying and applying the material while emphasizing its contribution to my expertise in IIoT.

The original diagram below outlines the IIoT Architecture, breaking it down into multiple layers that describe how data is transmitted, processed, and secured combining industries 3.0 and 4.0.

[**PDF Educational IIoT Architecture Diagram**](./Industrial%20IoT%20(IIoT)%20Architecture.pdf)

**Project covers key Industrial IoT (IIoT) layers, including**:
* Perception Layer (excluding actuators and PLCs)
* Edge Layer (featuring Azure IoT Edge)
* Network Layer (bi-directional data flow: Device-to-Cloud and Cloud-to-Device using MQTT and SSL/TLS protocols)
* Processing/Cloud Layer (data storage, device configuration, and IoT Edge module management)

---

> Due to the absence of a physical network adapter, I was unable to establish a network connection between EFLOW (Embedded Linux on Windows) for IoT Edge software and Raspberry Pi Pico-W. As a result, I divided the corresponding components (edge and sensor devices) into separate subprojects.

**Project Coverage (and subsequent content in order)**:
* **Communication between Raspberry Pi Pico-W (IoT Device) and Azure IoT Hub (Cloud) for transmitting sensor data via the MQTT protocol**
  * Industrial Temperature Sensor (Thermistor)
  * MQTT Fundamentals *(explained in detail below with a custom diagram from my protocol study)*
  * Secure Communication & Authentication *(Azure SSL/TLS compliance for MQTT connections)*
  * Ingesting Sensor Data from IoT Hub to Azure Storage Account
* **Deployment of IoT Edge Runtime (Software) for Linux on Windows (EFLOW) & Use of Edge Modules (IoT Docker Containers)**
  * Azure IoT Edge Fundamentals *(explained below with an outline diagram from my Azure IoT Edge study)*
  * Deployment of IoT Edge Runtime & Edge Modules
  * `SimulatedSensorData` Module
  * `Azure Stream Analytics (ASA)` Module

## Communication between Raspberry Pi Pico-W (IoT Device) and Azure IoT Hub (Cloud) for transmitting sensor data via the MQTT protocol
**Workflow**: Raspberry Pi Pico-W transmits thermistor sensor data to Azure IoT Hub over MQTT, secured with a DigiCert SSL/TLS certificate. The data is then stored in an Azure Storage Account container for further processing.
* **Industrial Temperature Sensor (Thermistor)**  
  A thermistor is a temperature-sensitive resistor that varies its resistance based on temperature changes
  
  Hardware connection with Pico
  <p align="left">
    <img src="https://drive.google.com/uc?export=view&id=1cy0sLBm8A5ls1qqRHGtBH8E_6l9k_AC-" width="400">
  </p>

---
  
* **MQTT Fundamentals**  
  To gain a detailed and nuanced understanding of the MQTT protocol and its Pub/Sub model, I created a custom technical diagram designed for quick study and easy navigation through key concepts.

  This diagram comprehensively covers all MQTT essentials, eliminating the need for additional external sources—provided the focus remains solely on this protocol.

  This work reflects my natural inclination toward structured and systematic thinking, which plays a crucial role in my approach to learning and in making architectural decisions.

  <p align="left">
    <img src="https://drive.google.com/uc?export=view&id=1QGvbcIgwhUwHezgaPoxMn51jf-6zyNjW" width="700">
  </p>
  
  [**JPEG Diagram**](./MQTT%20Essentials.jpg)

---

* **Secure Communication & Authentication**  
  For successful communication with Azure IoT Hub, the MQTT/AMQP protocol alone is not sufficient—SSL/TLS authentication and encryption are also required. Azure relies on DigiCert Certificate Authority for this purpose.

  However, this creates challenges when connecting Raspberry Pi Pico-W to IoT Hub, as newer versions of the MicroPython `umqtt.simple(or robust).MQTTClient` module no longer support SSL certification.  

  To address this limitation, a custom workaround has been implemented, adding this feature to the latest versions of the `umqtt` module:
  ```python
  import mip
  mip.install("umqtt.simple", index="https://pjgpetecodes.github.io/micropython-lib/mip/add-back-ssl-params")
  ```

  The certificate was obtained from the official [DigiCert website](https://www.digicert.com/kb/digicert-root) and is stored locally on the microcontroller.

  **The approach is implemented in the file:** [**picow_mqtt_iothub.py**](./picow_mqtt_iothub.py)

---

* **Receiving sensor data from IoT Hub to Azure Storage Account**

  * Thermistor and MQTT in action
    <p align="left">
      <img src="https://drive.google.com/uc?export=view&id=1TJK0zlAmjNjTqwczdY2k3hmPfQ7RY6HI" width="400">
    </p>
   
    <p align="left">
      <img src="https://drive.google.com/uc?export=view&id=1S8LD5ylWXpOmknLNh12AehkgOG6pQeX4" width="400">
    </p>
    
  * Recieved data
    <p align="left">
      <img src="https://drive.google.com/uc?export=view&id=1HuYCrrVXsKVxPxQhQkZQGjpd0F0uSN1U" alt="Thermistor Data" width="400">
    </p>

  * Directed data to storage
    <p align="left">
      <img src="https://drive.google.com/uc?export=view&id=122yaYXIVxltb-U8oP2RdIj9tFctcJwzb" alt="Thermistor Data" width="400">
    </p>
    
  * Acquisition, processing, and visualization of sensor data were carried out using Python libraries: Azure, Pandas, Matplotlib, and Seaborn
    <p align="left">
      <img src="https://drive.google.com/uc?export=view&id=1fzJu8HpqHkwJ7gNqSADGvrOtWbs-ebvi" alt="Thermistor Data" width="400">
    </p>
  
    **This work is also provided in the file:** [**picow_mqtt_iothub.py**](./azure-iot-project/retrieval_and_visualization.ipynb)

---

## Deployment of IoT Edge Runtime (software) for Linux on Windows (EFLOW) and Application of Edge Modules (IoT Docker Containers) such as `Azure Stream Analytics (ASA)` and `SimulatedSensorData`
* **Azure IoT Edge Fundamentals**  
  During the study of Azure IoT Edge technology, a quick summary diagram was created to provide a comprehensive view of its operational processes

  <p align="left">
    <img src="https://drive.google.com/uc?export=view&id=1QAHZRGCM9-nTsJXBONsx-pWqIjll8MV7" width="500">
  </p>
  
  [**JPEG Diagram**](./Azure%20IoT%20Edge.jpg)

  **Concise and Informative Overview:**
  
    An IoT Edge device operates through IoT Edge runtime software, which manages modules and overall system communication using two core components—Edge Agent and Edge Hub.
    * Edge Agent (Orchestrator) deploys, monitors, and manages modules (independent containers with distinct business logic) after the security layer IoT Edge Security Daemon, responsible for module certification and authentication. Edge Agent follows a JSON blueprint—deployment manifest—to execute these tasks.
    * Edge Hub (Manager) acts as a bridge (local proxy) between IoT Edge devices and Azure IoT Hub (cloud), facilitating local device-to-module and module-to-module communication via a brokering mechanism (device as a broker). Modules communicate independently (asynchronously), reducing latency and improving scalability and maintainability (updates, deletions, and additions do not cause disruptions).
    
    Understanding the development, deployment, and management of a module is simplified by four key concepts: Module Image, Module Instance, Module Twin, and Module Identity.
  
    Edge Module – A containerized application that performs specific functions
    * Module Image – A packaged software unit defining a module, stored as a container image in a repository. Each deployed image creates a unique instance per device.
    * ↑ Module Instance – A containerized computing unit running a module image on an IoT Edge device, managed by the IoT Edge runtime.
    * ↑ Module Twin – A JSON-based digital replica in IoT Hub, storing metadata, configuration, and state of a module instance with desired (from the deployment manifest) and reported (reflecting current conditions) properties.
    * ↑ Module Identity – Security credentials in IoT Hub associating a module instance with its identity, linking the instance to its twin.

---

* **Deployment of IoT Edge Runtime and Edge Modules**
  
    Linux is the preferred OS for deploying IoT Edge software on devices. In this project, Microsoft recommends using the built-in Hyper-V Virtual Machine (Windows Pro/Enterprise/IoT Enterprise) to deploy Linux on Windows (EFLOW – Embedded Linux on Windows).
    
    After installing EFLOW according to Microsoft's instructions, the next step is linking the virtual Linux machine to the created IoT Edge device in the “Device Management > Devices” section of Azure IoT Hub using its connection string (a key or set of credentials used to establish a secure connection).
    
    Once MQTT messages have been successfully exchanged, Edge module deployment becomes possible. This project utilizes two ready-made solutions provided by Azure: `SimulatedTemperatureSensor`, `Stream Analytics`
    
    * `SimulatedTemperatureSensor` module simulates real industrial conditions, recording the machine’s temperature, atmospheric pressure, and the temperature & humidity of the room.
    
    * `Stream Analytics` module resets the machine’s temperature after exceeding 70°C, triggering an alert message in IoT Hub, thus enabling communication between the two modules.
    
    With an available repository, deploying a module via the deployment manifest takes under a minute in the “Set modules” section of the IoT Edge device—unless manual configuration of Environment Variables or Module Twin Settings is required. Deployment on the device occurs automatically.
    
    The current EFLOW setup displays deployed Edge modules along with their status (running/stopped), description (runtime), and configuration details (container images).
      <p align="left">
        <img src="https://drive.google.com/uc?export=view&id=1MQRGVeCN-w9ykN7u37xvYiXKDTo1HjD5" width="600">
      </p>

  ---

* **`SimulatedSensorData` Module**
  
  Simulation results for sensor data
      <p align="left">
        <img src="https://drive.google.com/uc?export=view&id=1EMB6BjKjqREQTKrqOp18GOTLyURujDPc" width="500">
      </p>
  
  The Environment Variables functionality was utilized to modify variable values in the module image copy on the Edge device. These values are transmitted in the deployment manifest (a guiding JSON script for the Edge Agent)
      <p align="left">
        <img src="https://drive.google.com/uc?export=view&id=1mQJTp4tJ60wzntkxFwV9L8uRmPy_VzIF" width="600">
      </p>

---

* **`Azure Stream Analytics (ASA)` Module**
  
    This module enables real-time data processing and analytics directly on edge devices, utilizing SQL-based queries to filter, aggregate, and transform data.
    
    At its core, ASA operates around the concept of a “Job”—a unique analytical entity responsible for executing data processing logic. The job is first created within the Stream Analytics job resource and then deployed on an Edge device via the “Set modules” section.
    
    Each job is assigned Input and Output values, which are later integrated into SQL-based processing. Initially, these values serve only as placeholders—they remain empty until actively used within routing mechanisms (direct messages enabling module-to-module communication).
    
    SQL query example demonstrating Input and Output values in action:
    ```sql
    FROM temperature                       -- 1.
    TIMESTAMP BY timeCreated               -- 2. Uses sensor event timestamps for accuracy instead of system ingestion time  
    GROUP BY TumblingWindow(second, 30)    -- 3. Creates a sliding 30-second data window, defining the scope for calculations  
    HAVING AVG(machine.temperature) > 70   -- 4. Aggregates machine temperature within the window  
    SELECT 'reset' AS command              -- 5. When the average temperature exceeds 70°C within the last 30 seconds, the 'reset' value is assigned to the 'command' variable  
    INTO alert                             -- 6. The 'reset' value is sent via the Output route 'alert'; if no action is needed, the job continues generating SQL queries  
    ```
    
    <p align="left">
      <img src="https://drive.google.com/uc?export=view&id=14PsZoT71s7N0B82Tl0mCsCIGh_vlKoVG" width="600">
    </p>

    In an IoT Edge device, module-to-module communication is configured in the “Set modules > Routes” section. These routes define how sensor data and alert messages flow between modules and the cloud.
    
    Defined Routes:
    * `telemetryToCloud` – Standard transmission of sensor data to the cloud.  
      *`$upstream` refers to device-to-cloud (D2C) data transmission using MQTT/AMQP protocols, whereas `$downstream` refers to cloud-to-device (C2D) communication.
    * `telemetryToAsa` – Sends all sensor data (not just temperature) to the ASA module at the Input endpoint “temperature”.  
      *BrokeredEndpoint() serves as an internal message routing mechanism for this process.
    * `alertsToCloud` – If the SQL-based logic triggers an alert, the message is sent to IoT Hub for further processing or action.
    * `alertsToReset` – In the same scenario, the `SimulatedTemperatureSensor` module receives a ‘reset’ value at its ‘control’ intake, leading to the machine temperature being reset.

    <p align="left">
      <img src="https://drive.google.com/uc?export=view&id=1vAD06yq7GhH6c04A2URH49BARXynDHLX" width="600">
    </p>

    Here's what it looks like in practice
  
    <p align="left">
      <img src="https://drive.google.com/uc?export=view&id=1E7kcRn7XVaIP4a_Wr9Am6Wkpq2uipgME" width="600">
    </p>

    <p align="left">
      <img src="https://drive.google.com/uc?export=view&id=1QFPZlMSaPSHCvUynTJMy4HPa9HFpTO0U" width="600">
    </p>

---

  **That's all from me 😀, thank you for your attention!**  
  I hope I have taught you something.

  [**Minimalist Portfolio**](https://dvyemchuk.short.gy/portfolio)  
  dvyemchuk@gmail.com
