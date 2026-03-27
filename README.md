# 🌱 FarmGuard AI: Intelligent Agrivoltaics & Carbon Capture Using Multi-Agent
<h2>Project Name</h2>
FarmGuard AI: Intelligent Agrivoltaics & Carbon Capture
<h2>Description</h2>
<p align="center">
  <img src="LOGO.png" width="300">
</p>

## Overview

FarmGuard AI is an **AI-powered climate technology platform** that enables **small farmers and renewable energy producers to participate in the global carbon credit economy**.

Industries across the world generate significant **greenhouse gas emissions** and rely on carbon credits to achieve **Net Zero and ESG goals**. Meanwhile, millions of farmers naturally capture carbon through trees, vegetation, and sustainable agricultural practices — but are unable to benefit due to **high verification costs, complex calculations, and lack of access to carbon markets**.

FarmGuard AI solves this problem using a **multi-agent AI system** that automates the entire carbon credit lifecycle:

-  Carbon measurement  
-  Scientific calculation  
-  AI-based validation  
-  Automated audit documentation  
-  Marketplace connection  

By combining **satellite imagery, AI models, IoT data, and Microsoft AI technologies**, the platform converts environmental impact into **verified, transparent, and tradable carbon credits**.

##  Key Capabilities

-  Detects trees and vegetation using satellite images  
-  Analyzes crop health using NDVI  
-  Calculates biomass, carbon, and CO₂  
-  Estimates avoided emissions from solar energy  
-  Validates data using AI (detects errors/fraud)  
-  Generates automatic audit reports (AI + IoT)  
-  Connects farmers with companies to sell carbon credits  

This significantly reduces verification costs and empowers farmers to generate **sustainable income while contributing to global climate action**.

## Problem Statement

Climate change is increasing due to high pollution from industries.  
Companies release large amounts of **greenhouse gases** and need to buy **carbon credits** to reduce their impact.

At the same time, farmers naturally help the environment by growing **trees, crops, and using renewable energy like solar**.

However, small farmers cannot benefit from carbon credits because:

-  They don’t know their land can earn carbon credits  
-  Carbon verification is expensive  
-  Calculations are complex and technical  
-  Audit documentation is difficult  
-  No direct access to companies or markets  

Because of this, millions of farmers are unable to earn income from their environmental contribution.

There is a need for a **simple, low-cost system** that helps farmers generate and sell **verified carbon credits easily**.


##  Solution

FarmGuard AI is a **multi-agent AI platform** with **multi-language support** that enables farmers to easily participate in the carbon credit ecosystem.

It provides a **single platform** that connects farmers, solar producers, and companies, removing the need for complex tools and manual processes.

---

###  Who Uses the Platform

####  Farmers
- Register land using map or documents  
- Upload farm or tree images  
- View carbon reports and earnings  

####  Solar Producers
- Upload solar generation data  
- Track avoided emissions and credits  

####  Companies
- Explore verified carbon credits  
- Purchase directly through the platform  

---

### 🤖 How the System Works

- Uses satellite and image data to analyze farms  
- Processes environmental data using AI models  
- Uses IoT sensor data for better validation  
- Generates ready-to-use audit reports automatically  
- Provides a simple dashboard for tracking credits and income  



## Multi-Agent AI Workflow (Semantic Kernel)
FarmGuard AI uses a **multi-agent architecture orchestrated with Microsoft Semantic Kernel** to automate carbon credit generation, validation, documentation, and marketplace connection for farmers, solar producers, and companies.

###  End-to-End Workflow

1. **Farmer Data Input**  
   Farmers upload land details, images, or sensor data.

2. **Orchestrator Agent**  
  Controls the overall workflow and decides which agent should act next using **Semantic Kernel orchestration**.

3. **Vision Agent**  
   Uses **satellite imagery and Azure AI Vision** to detect trees, vegetation, and land conditions.

4. **Carbon Analyst Agent**  
   Calculates biomass, carbon storage, CO₂ equivalent, and estimated carbon credits.
   
##### Tree-based Carbon Credit Calculation
Above-Ground Biomass (AGB):
```
AGB = 0.0673 × (ρ × DBH² × H)^0.976
```
Where:
- ρ = wood density  
- DBH = diameter at breast height  
- H = tree height  
Simplified estimation:
```
Biomass ≈ 0.25 × H²
```
Carbon stored:
```
Carbon = Biomass × 0.5
```
CO₂ equivalent:
```
CO₂ = Carbon × 3.67
```
Carbon credits:
```
Credits = CO₂ / 1000
```
##### Solar Carbon Credit Calculation
Avoided emissions:
```
Avoided CO₂ = Solar Energy Generated (kWh) × Grid Emission Factor
```
Carbon credits:
```
Credits = Avoided CO₂ / 1000
```
This allows the platform to calculate carbon credits for both **tree-based sequestration and renewable energy generation**.

5. **Validation Agent**  
   Checks for **anomalies, incorrect reporting, sudden spikes, and possible fraud** in environmental or farm data.

6. **AI + IoT Documentation**  
   Generates audit-ready reports using AI analysis and environmental sensor data.

7. **Blockchain Layer**  
   Stores verified carbon credit records securely and ensures data integrity.

8. **Market Agent**  
   Connects verified carbon credits with companies for purchase.

---

###  Output

- Verified Carbon Credits  
- Audit-Ready Documentation  
- Marketplace Integration  


## System Architecture

FarmGuard AI uses a **multi-layer architecture** that connects farmers, solar producers, and companies through AI-driven automation.
The platform combines:
- Satellite imagery
- Renewable energy data
- AI agents
- IoT-supported verification
- Blockchain-based carbon credit records

<p align="center">
<img src="./Architecture.png" width="800">
</p>

### Architecture Explanation
The FarmGuard AI architecture consists of several layers that work together to automate carbon credit generation and trading.
#### 1. User Applications Layer
The platform provides three main user interfaces:
- **Farmers App** – Farmers upload tree and land information.
- **Homeowners / Solar Producers App** – Solar energy producers upload solar generation data.
- **Company Portal** – Companies browse and purchase verified carbon credits.
These applications allow different stakeholders to interact with the system.
#### 2. AI Orchestration Layer
At the center of the system is **Microsoft Semantic Kernel**, which acts as the **agent orchestrator**.
Semantic Kernel manages communication between different AI agents and ensures that the workflow runs in the correct sequence.
#### 3. AI Processing Layer
The platform uses specialized AI agents for different tasks:
- **Vision Agent** – Detects trees and vegetation using satellite imagery.
- **Carbon Agent** – Calculates biomass, carbon storage, and carbon credits.
- **Energy Agent** – Calculates avoided emissions from solar energy systems.
- **Validation Agent** – Detects anomalies or incorrect environmental data.
- **Market Agent** – Connects verified credits with companies that want to buy them.
These agents work together to automate environmental analysis.
#### 4. Data Analysis Layer
FarmGuard AI integrates multiple environmental data sources:
- **Azure AI Vision** – analyzes satellite images
- **Sentinel-2 satellite data (Sentinel Hub)** – vegetation and land monitoring
- **Google Maps** – farmer land registration and geolocation
- **Solar production data** – renewable energy emission reduction analysis
These data sources provide the environmental evidence needed for carbon calculations.
#### 5. Documentation & Verification Layer
FarmGuard AI automatically generates **audit-ready carbon verification documents** using **AI and IoT data**.
The documentation includes:
- satellite image evidence
- vegetation analysis
- carbon credit calculations
- environmental monitoring data
This significantly reduces the cost of traditional carbon credit auditing.
#### 6. Blockchain Layer
The **Blockchain Agent** records verified carbon credits and ownership information in a secure ledger.
Blockchain provides:
- tamper-proof records
- transparent transactions
- trusted carbon credit ownership
#### 7. Data Storage Layer
The system stores important platform data including:
- farmer land information
- carbon credit calculations
- verification documentation
- transaction history
## Technologies Used
### Backend Technologies
The backend of FarmGuard AI powers AI orchestration, carbon credit calculations, satellite analysis, verification workflows, and marketplace connectivity.
- **Python(3.12.6)**  
  Core backend programming language used to implement AI agents, carbon credit calculations, and system logic.
- **FastAPI**  
  High-performance Python framework used to build backend APIs for communication between the frontend interface and AI services.
- **Microsoft Semantic Kernel**  
  Orchestrates the multi-agent AI workflow and manages communication between agents such as Vision Agent, Carbon Analyst Agent, Validation Agent, and Market Agent.
- **Azure OpenAI Service**  
  Provides natural language understanding, reasoning, report generation, and intelligent agent decision-making.
- **Azure AI Vision**  
  Analyzes satellite imagery to detect trees, vegetation cover, crop health, and land-use changes.
- **Sentinel-2 Satellite Data (Sentinel Hub)**  
  Provides high-resolution satellite imagery used for vegetation monitoring and NDVI analysis to estimate biomass and carbon sequestration.
- **IoT Integration**  
  Environmental sensors provide monitoring data such as soil conditions and climate parameters for audit-ready documentation.
- **Blockchain Integration**  
  Stores verified carbon credit records, ownership proof, and transaction history in a secure and tamper-proof ledger.
- **Carbon Calculation Engine (IPCC Methodology)**  
  Implements biomass estimation, carbon conversion, and avoided emission formulas for generating carbon credits.
### Frontend Technologies
The frontend interface enables farmers, solar producers, and companies to interact with the FarmGuard AI platform.
- **HTML5**  
  Structures the web interface and user dashboards.
- **CSS**  
  Provides responsive and modern UI design.
- **JavaScript**  
  Enables dynamic interaction between the user interface and backend APIs.
- **Google Maps API**  
  Allows farmers to register their land by selecting geographic locations directly on the map.
- **Solar Energy Data (Google Cloud Console)**  
  Solar generation data is retrieved and processed to calculate avoided emissions and solar-based carbon credits.
### Development Tools
- **Git & GitHub** – Version control and project repository  
- **Visual Studio Code** – Development environment  
- **Draw.io** – Architecture diagram creation
## Key Features
FarmGuard AI provides several powerful capabilities that make carbon credit generation accessible to farmers and renewable energy producers.
- **Automated Carbon Credit Calculation**  
  Uses AI models and IPCC methodologies to calculate carbon sequestration from trees and avoided emissions from solar energy.
- **Satellite-Based Environmental Monitoring**  
  Integrates Sentinel-2 satellite data via Sentinel Hub to detect vegetation, monitor land conditions, and analyze NDVI.
- **Multi-Agent AI Architecture**  
  Uses Microsoft Semantic Kernel to orchestrate specialized AI agents for vision analysis, carbon calculation, validation, documentation, and marketplace matching.
- **AI-Powered Fraud Detection**  
  Validation agents detect anomalies, suspicious data patterns, and potential reporting errors.
- **Automated Audit Documentation**  
  Combines AI analysis with IoT environmental data to generate verification-ready carbon reports.
- **Blockchain-Based Carbon Credit Records**  
  Stores carbon credit ownership and transaction history securely to ensure transparency and trust.
- **Integrated Carbon Marketplace**  
  Connects farmers and solar producers directly with companies looking to purchase verified carbon credits.
- **Land Registration via Map Interface**  
  Uses Google Maps to allow farmers to easily register their land and agricultural assets.
  ## Why FarmGuard AI is Unique

- **Multi-Agent AI Architecture**  
  Uses Microsoft Semantic Kernel to orchestrate multiple AI agents that automate carbon credit generation, validation, and marketplace operations.

- **Satellite-Based Carbon Monitoring**  
  Integrates Sentinel-2 satellite data via Sentinel Hub and NDVI analysis to detect vegetation health and estimate carbon sequestration.

- **Automated Carbon Verification**  
  Combines AI analysis with IoT environmental monitoring to generate **audit-ready documentation**, reducing verification costs for farmers.

- **Unified Carbon Marketplace**  
  Connects **farmers, solar producers, and companies** on a single platform to generate and trade carbon credits transparently.

- **Blockchain-Based Trust System**  
  Stores carbon credit ownership and transaction records in a **tamper-proof blockchain ledger**, improving transparency and trust.

- **Future Carbon Capture Innovation**  
  Plans to integrate **microalgae carbon capture systems** to absorb CO₂ and methane while generating additional carbon credits.
## Future Scope

- **Microalgae Carbon Capture**  
  Integrate microalgae cultivation systems to capture additional CO₂ and methane while generating extra carbon credits for farmers.

- **NGO Collaboration**  
  Partner with agricultural and environmental NGOs to educate farmers, promote sustainable practices, and support platform adoption in rural areas.

- **Carbon Certification & Verification**  
  Integrate with third-party auditors and global carbon registries such as **Verra** and **Gold Standard** to ensure internationally recognized carbon credit certification.

- **Global Platform Expansion**  
  Scale the platform to support **millions of farmers, renewable energy producers, and corporate sustainability programs worldwide**.

  ## Business Impact

- Reduces carbon verification cost by up to 80%
- Enables farmers to earn additional income
- Helps companies achieve ESG and Net Zero goals
- Creates a transparent carbon marketplace  

### Visualization
#### Platform Overview

<p align="center">
<img src="./demo-p1.png" width="700">
</p>

#### Farmer Dashboard

<p align="center">
<img src="./demo-p2.png" width="700">
</p>


### Conclusion
FarmGuard AI demonstrates how **AI, satellite monitoring, and intelligent agent systems** can transform the carbon credit ecosystem.
By automating carbon measurement, verification, and marketplace access, the platform makes the carbon economy accessible to **small farmers, renewable energy producers, and sustainability-focused companies**.
Through **Microsoft AI technologies, satellite data, and multi-agent orchestration**, FarmGuard AI provides a scalable solution for **climate action, sustainable agriculture, and transparent carbon credit generation**.
## Project URL
https://github.com/Bhavana-sree/farmguard-ai-using-multiagent

## 🎥 Demo Videos

### 1️⃣ Complete Platform Demo 
https://youtu.be/dSF2wshk09Q?si=a0ie5H18kWZwEQ70

### 2️⃣ Problem & Solution Explanation
https://youtu.be/lW2vDOKTd1w

## Team
**Team Name:** Quantum Minds
Members:
- Bhavanasree B
- Sowmya N

Hackathon: **Microsoft AI Dev Days Hackathon**
