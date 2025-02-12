import re
from babel.numbers import format_currency
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from streamlit_autorefresh import st_autorefresh


refresh_interval = 60 * 1000  # 60 seconds
st_autorefresh(interval=refresh_interval, key="refresh")


pd.set_option("display.max_columns", None)

def scrape_shakti_cloud_pricing():
    url = "https://shakticloud.ai/pricing.html"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        gpu_data = []

       
        pricing_cards = soup.find_all("div", class_="awp-card")
        for card in pricing_cards:
            plan_name = card.find("span", class_="card-para sb")
            plan_name = plan_name.text.strip() if plan_name else "N/A"
            gpu_info = card.find("p", text=lambda x: x and "GPU :" in x)
            if gpu_info:
                gpu_details = gpu_info.text.replace("GPU :", "").strip()
                gpu_parts = gpu_details.split(" x ")
                if len(gpu_parts) == 2:
                    gpu_count = gpu_parts[0].strip()
                    gpu_model = gpu_parts[1].strip()
                else:
                    gpu_count = "N/A"
                    gpu_model = gpu_details.strip()
            else:
                gpu_model = "N/A"
                gpu_count = "N/A"
            cpu_info = card.find("p", text=lambda x: x and "CPU :" in x)
            cpu_cores = cpu_info.text.replace("CPU :", "").strip() if cpu_info else "N/A"

            ram_info = card.find("p", text=lambda x: x and "RAM :" in x)
            ram = ram_info.text.replace("RAM :", "").strip() if ram_info else "N/A"

            storage_info = card.find("p", text=lambda x: x and "Storage :" in x)
            storage = storage_info.text.replace("Storage :", "").strip() if storage_info else "N/A"

            bandwidth_info = card.find("p", text=lambda x: x and "Bandwidth" in x)
            bandwidth = bandwidth_info.text.strip() if bandwidth_info else "N/A"

            price_info = card.find("span", class_="c-title grey1")
            price = price_info.text.strip() if price_info else "N/A"

            gpu_data.append({
                "Plan Name": plan_name,
                "GPU Model": gpu_model,
                "GPU Count": gpu_count,
                "CPU Cores": cpu_cores,
                "RAM": ram,
                "Storage": storage,
                "Internet Bandwidth": bandwidth,
                "Price (Per Hour)": price
            })


        return gpu_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Shakti Cloud: {e}")
        return []



def scrape_coreweave_pricing():
    url = "https://www.coreweave.com/pricing"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        gpu_data = []

        table_rows = soup.find_all("div", class_="table-grid")

        for row in table_rows:
            model_tag = row.find("h3", class_="table-model-name")
            gpu_model = model_tag.text.strip() if model_tag else "N/A"

            price_tag = row.find("div", id=lambda x: x and "w-node-_2a00e7fa" in x)
            gpu_price = price_tag.text.strip() if price_tag else "N/A"

            vram_tag = row.find("div", id=lambda x: x and "w-node-_5a709234" in x)
            vram = vram_tag.text.strip() if vram_tag else "N/A"

            vcpus_tag = row.find("div", id=lambda x: x and "w-node-f5a7a2eb" in x)
            vcpus = vcpus_tag.text.strip() if vcpus_tag else "N/A"

            storage_tag = row.find("div", id=lambda x: x and "w-node-_86e3bb3b" in x)
            local_storage = storage_tag.text.strip() if storage_tag else "N/A"

            ram_tag = row.find("div", text="System RAM")
            system_ram = ram_tag.find_previous_sibling("div").text.strip() if ram_tag else "N/A"

            gpu_count_tag = row.find("div", id=lambda x: x and "w-node-_9c135cbf" in x)
            gpu_count = gpu_count_tag.text.strip() if gpu_count_tag else "N/A"

            gpu_data.append({
                "GPU Model": gpu_model,
                "Price": gpu_price,
                "VRAM (GB)": vram,
                "vCPUs": vcpus,
                "Local Storage (TB)": local_storage,
                "System RAM": system_ram,
                "GPU Count": gpu_count
            })

        return gpu_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from CoreWeave: {e}")
        return []





# Function to scrape Shakti Cloud pricing
def scrape_shakti_cloud_price():
    url = "https://shakticloud.ai/pricing.html"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        gpu_data = []

        pricing_tables = soup.find_all("div", class_="pricing-table-responsive")
        for table in pricing_tables:
            rows = table.find("tbody").find_all("tr")
            for row in rows:
                plan_cell = row.find("td")
                if plan_cell:
                    plan_details = plan_cell.get_text(strip=True)
                    pricing_cells = row.find_all("td")[1:]
                    prices = [cell.get_text(strip=True) for cell in pricing_cells]

                    gpu_data.append({
                        "Plan Details": plan_details,
                        "On-demand": prices[0] if len(prices) > 0 else "N/A",
                        "Monthly Contract": prices[1] if len(prices) > 1 else "N/A",
                        "6 Months Contract": prices[2] if len(prices) > 2 else "N/A",
                        "12 Months Contract": prices[3] if len(prices) > 3 else "N/A",
                        "24 Months Contract": prices[4] if len(prices) > 4 else "N/A",
                        "36 Months Contract": prices[5] if len(prices) > 5 else "N/A",
                        "48 Months Contract": prices[6] if len(prices) > 6 else "N/A",
                    })

        return gpu_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Shakti Cloud: {e}")
        return []



def scrape_replicate_pricing():
    url = "https://replicate.com/pricing"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        pricing_data = []
        rows = soup.select("tbody tr.border-b")

        for row in rows:
            name_tag = row.find("span", class_="font-bold")
            hardware_name = name_tag.text.strip() if name_tag else "N/A"
            id_tag = row.find("span", class_="font-mono text-r8-gray-11")
            hardware_id = id_tag.text.strip() if id_tag else "N/A"
            price_cell = row.find("td", class_="font-mono")
            if price_cell:
                per_second_price = price_cell.text.split("\n")[0].strip()
                per_hour_price_tag = price_cell.find("span", class_="text-r8-gray-11")
                per_hour_price = per_hour_price_tag.text.strip() if per_hour_price_tag else "N/A"
            else:
                per_second_price = "N/A"
                per_hour_price = "N/A"
            quantity_cells = row.find_all("td", class_="font-mono")
            gpu_quantity = quantity_cells[1].text.strip() if len(quantity_cells) > 1 else "N/A"
            cpu_quantity = quantity_cells[2].text.strip() if len(quantity_cells) > 2 else "N/A"
            gpu_ram = quantity_cells[3].text.strip() if len(quantity_cells) > 3 else "N/A"
            system_ram = quantity_cells[4].text.strip() if len(quantity_cells) > 4 else "N/A"

            pricing_data.append({
                "Hardware Name": hardware_name,
                "Hardware ID": hardware_id,
                "Per-Second Price": per_second_price,
                "Per-Hour Price": per_hour_price,
                "GPU Quantity": gpu_quantity,
                "CPU Quantity": cpu_quantity,
                "GPU RAM": gpu_ram,
                "System RAM": system_ram,
            })

        return pricing_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Replicate: {e}")
        return []



def scrape_together_ai_pricing():
    url = "https://www.together.ai/pricing"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        rows = soup.find_all('li', class_='pricing_content-row-2')



        together_ai_data = []
        for row in rows:
            columns = row.find_all('div', class_='pricing_content-cell')
            hardware = columns[0].get_text(strip=True)
            price = columns[1].get_text(strip=True)
            together_ai_data.append([hardware, price])

        return together_ai_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Together.ai: {e}")
        return []




def scrape_digitalocean_gpu_pricing():
    url = "https://www.digitalocean.com/pricing/gpu-droplets"  

    

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        digitalo_data = []


        pricing_cards = soup.find_all("div", class_="CardPricingstyles__StyledCardPricingCard-sc-1c4kjfb-1") 

        for card in pricing_cards:

            gpu_model_element = card.find("h3", class_="Typographystyles-sc-o7qsl9-0")
            gpu_model_text = gpu_model_element.text.strip() if gpu_model_element else "N/A"


            gpu_model_text = gpu_model_text.replace("NVIDIA", "Nvidia")


            if gpu_model_text != "N/A" and "x" in gpu_model_text:
                gpu_model_parts = gpu_model_text.split("x")
                gpu_model = gpu_model_parts[0].strip()
                gpu_count = int(gpu_model_parts[1].strip())
            else:
                gpu_model = gpu_model_text
                gpu_count = 1


            price_element = card.find("span", class_="Typographystyles-sc-o7qsl9-0 hMOZOB")
            price = price_element.text.strip() if price_element else "N/A"


            if price != "N/A":
                price = f"${float(price.replace('$', '').replace(',', '')):,.2f}"

            specs = card.find_all("li")
            gpu_memory = specs[1].find("span", class_="Typographystyles-sc-o7qsl9-0 cskSii").text.strip() if len(specs) > 1 else "N/A"
            droplet_memory = specs[2].find("span", class_="Typographystyles-sc-o7qsl9-0 cskSii").text.strip() if len(specs) > 2 else "N/A"
            vcpus = specs[3].find("span", class_="Typographystyles-sc-o7qsl9-0 cskSii").text.strip() if len(specs) > 3 else "N/A"

            digitalo_data.append({
                "GPU Model": gpu_model,
                "GPU Count": gpu_count,
                "Price": price,
                "GPU RAM": gpu_memory,
                "Source": "DigitalOcean"
            })


        return digitalo_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Together.ai: {e}")
        return []


def scrape_runpod_gpu_pricing():
    url = "https://www.runpod.io/pricing" 
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")


    gpu_items = soup.find_all('div', class_='MuiStack-root css-q3nr5k')

    gpu = []
    for item in gpu_items:

        gpu_model = item.find('div', class_='MuiTypography-root MuiTypography-body1 css-6ukrhs')
        gpu_ram = item.find_all('div', class_='MuiTypography-root MuiTypography-body1 css-1xqiyyp')
        price_tag = item.find_all('div', class_='MuiTypography-root MuiTypography-body1 css-c16693')
        if gpu_model and gpu_ram and price_tag:
            gpu_model = gpu_model.get_text(strip=True)
            gpu_count = 1
            if "x" in gpu_model:
                gpu_count = int(gpu_model.split("x")[0].strip())
                gpu_model = gpu_model.split("x")[1].strip()
            gpu_ram_total = gpu_ram[1].get_text(strip=True) if len(gpu_ram) > 1 else "N/A"
            gpu_ram_total = gpu_ram_total.split()[0] if "GB" in gpu_ram_total else "N/A"

            price = price_tag[0].get_text(strip=True)
            gpu.append([gpu_model.strip(), gpu_count, gpu_ram_total.strip(), price.strip()])

    return gpu


def scrape_nebius_gpu_pricing():
    url = "https://nebius.com/prices"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('div', class_='pc-table__table')
    rows = table.find_all('div', class_='pc-table__row')

    nebius_data = []

    for row in rows:
        gpu_model = row.find('div', class_='pc-table__cell_justify_left')
        gpu_model = gpu_model.text.strip() if gpu_model else "N/A"
        if 'x' in gpu_model:
            gpu_count = int(gpu_model.split('x')[0].strip())
        else:
            gpu_count = 1
        if 'H100' not in gpu_model and 'L40s' not in gpu_model:
            continue

        if 'H100' in gpu_model:
            gpu_model = "Nvidia H100"
        elif 'L40s' in gpu_model:
            gpu_model = "Nvidia L40S"

        vram = row.find_all('div', class_='pc-table__cell_justify_right')[0].text.strip()
        ram = row.find_all('div', class_='pc-table__cell_justify_right')[1].text.strip()
        vcpus = row.find_all('div', class_='pc-table__cell_justify_right')[2].text.strip()

        price_on_demand = row.find_all('div', class_='pc-table__cell_justify_right')[3].text.strip()
        price_reserve = row.find_all('div', class_='pc-table__cell_justify_right')[4].text.strip()


        price_on_demand = format_currency(float(price_on_demand.replace('$', '').replace(',', '').strip()), 'USD', locale='en_US')
        price_reserve = format_currency(float(price_reserve.replace('$', '').replace(',', '').strip()), 'USD', locale='en_US')

        nebius_data.append([gpu_model, gpu_count, price_on_demand,vram, "Nebius"])


    return nebius_data


def save_to_dataframe(data):
    df = pd.DataFrame(data)
    return df
def add_node_column(df):
    if "Node" not in df.columns:
        df["Node"] = ""

    df["GPU Count"] = pd.to_numeric(df["GPU Count"], errors="coerce").fillna(0).astype(int)

    def calculate_node(row):
        if pd.notna(row["GPU Model"]):  # Ensure GPU Model is not NaN
            if "H100" in row["GPU Model"]:
                return row["GPU Count"] // 8 if row["GPU Count"] >= 8 else 0  # H100: Multiple of 8
            elif "L40S" in row["GPU Model"]:
                return row["GPU Count"] // 4 if row["GPU Count"] >= 4 else 0  # L40S: Multiple of 4
        return 0  # Default to 0 for other GPUs

    df["Node"] = df.apply(calculate_node, axis=1).astype(str)
    return df


# 🔹 **Function to Filter GPU Data**
def filter_gpu_data(df, gpu_name, gpu_count=None, node=None):
    filtered_df = df

    if gpu_name:
        filtered_df = filtered_df[filtered_df["GPU Model"].str.contains(gpu_name, case=False, na=False)]
    if gpu_count:
        filtered_df = filtered_df[filtered_df["GPU Count"] == gpu_count]
    if node:
        filtered_df = filtered_df[filtered_df["Node"].str.contains(node, case=False, na=False)]

    return filtered_df


combined_df = pd.DataFrame(columns=["GPU Model", "GPU Count", "Price", "GPU RAM", "Source", "Node"])
def main():
    global combined_df 
    st.title("GPU Cloud Pricing Comparison")
   
    # Initialize combined DataFrame
    combined_df = pd.DataFrame(columns=["GPU Model", "GPU Count", "Price", "GPU RAM", "Source", "Node"])  # Include Node column


    # Shakti Cloud Pricing Data
    shakti_cloud_data = scrape_shakti_cloud_pricing()
    if shakti_cloud_data:
        df_s2 = save_to_dataframe(shakti_cloud_data)

        df_s3 = df_s2[df_s2["GPU Model"].str.contains("NVIDIA H100|NVIDIA L40S", case=False, na=False)]
        df_s3 = df_s3[["GPU Model", "GPU Count", "Price (Per Hour)", "RAM"]]
        df_s3.rename(columns={"Price (Per Hour)": "Price"}, inplace=True)

        df_s3["GPU Count"] = pd.to_numeric(df_s3["GPU Count"], errors="coerce")  # Keep NaN for invalid values

        df_s3_filtered = df_s3[
            (
                (df_s3["GPU Model"].str.contains("Nvidia H100", case=False)) &
                (df_s3["GPU Count"].isin([1, 2, 3, 4, 5, 6, 7, 8]))
            ) |
            (
                (df_s3["GPU Model"].str.contains("Nvidia L40S", case=False)) &
                (df_s3["GPU Count"].isin([1, 2, 3, 4, 5, 6, 7, 8]))
            )
        ]

        df_s3_filtered = df_s3_filtered.drop_duplicates(subset=["GPU Model"]).reset_index(drop=True)

        df_s3_filtered['GPU Model Name'] = df_s3_filtered['GPU Model'].str.extract(r'([^(\n]+)')
        df_s3_filtered['GPU RAM'] = df_s3_filtered['GPU Model'].str.extract(r'\((.*?)\)')

        df_s3_filtered = df_s3_filtered.drop(columns=["GPU Model"])
        df_s3_filtered.rename(columns={"GPU Model Name": "GPU Model"}, inplace=True)

        df_s3_filtered = df_s3_filtered.drop(columns=["RAM"])
        df_s3_filtered = df_s3_filtered[["GPU Model", "GPU Count", "Price", "GPU RAM"]]

        df_s3_filtered['Price'] = df_s3_filtered['Price'].replace({'\$': '', ',': ''}, regex=True)
        df_s3_filtered['Price'] = pd.to_numeric(df_s3_filtered['Price'], errors='coerce')
        df_s3_filtered['Price'] = df_s3_filtered['Price'].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "")

        df_s3_filtered['GPU Model'] = df_s3_filtered['GPU Model'].str.replace('Nvidia L40s', 'Nvidia L40S')
        df_s3_filtered['Source'] = 'Shakti Cloud'  # Add source column

        # Append to combined_df
        combined_df = pd.concat([combined_df, df_s3_filtered], ignore_index=True)



    # CoreWeave Pricing Data
    coreweave_data = scrape_coreweave_pricing()
    if coreweave_data:
        df2 = save_to_dataframe(coreweave_data)
        df3 = df2[df2["GPU Model"].isin(["NVIDIA HGX H100", "NVIDIA L40S"])]
        df3 = df3[["GPU Model", "GPU Count", "Price", "VRAM (GB)"]]
        df3.rename(columns={"VRAM (GB)": "GPU RAM"}, inplace=True)

        df3["GPU Count"] = pd.to_numeric(df3["GPU Count"], errors="coerce")  # Keep NaN for invalid values

        df3 = df3.drop_duplicates(subset=["GPU Model"])
        df3['GPU Model'] = df3['GPU Model'].str.replace(r'NVIDIA HGX H100', 'Nvidia H100', regex=True)
        df3['GPU Model'] = df3['GPU Model'].str.replace(r'NVIDIA L40S', 'Nvidia L40S', regex=True)
        df3 = df3.reset_index(drop=True)
        df3['Price'] = df3['Price'].astype(str).str.replace('[^\d.]', '', regex=True)
        df3['Price'] = pd.to_numeric(df3['Price'], errors='coerce')
        df3['Price'] = df3['Price'].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "")

        df3['Source'] = 'CoreWeave'  # Add source column
        combined_df = pd.concat([combined_df, df3], ignore_index=True)



    # Additional Shakti Cloud Pricing Data
        shakti_cloud_data1 = scrape_shakti_cloud_price()

        if shakti_cloud_data1:
    # Convert scraped data into a DataFrame directly
            df_b = pd.DataFrame(shakti_cloud_data1)

    # Ensure the required column exists
            if "Plan Details" in df_b.columns:
                df_b = df_b[df_b["Plan Details"].str.contains(
                    "NVIDIA H100|NVIDIA L40S|Baremetal.*?H100 HGX|Bare Metal L40S|SHAKTI CLOUD - H100 HGX Cluster|SHAKTI CLOUD - L40S Cluster",
                    case=False,
                    na=False
                )]

        # Rename columns
                df_b.rename(columns={"Plan Details": "GPU Model", "On-demand": "Price"}, inplace=True)

        # Ensure 'GPU Model' column is of type string, handle NaN values
                df_b["GPU Model"] = df_b["GPU Model"].fillna('').astype(str)

        # Check if 'GPU Model' is now a series and apply str operations
                if isinstance(df_b["GPU Model"], pd.Series):
            # Extract GPU Count
                    df_b["GPU Count"] = (
                        df_b["GPU Model"]
                        .str.extract(r"(\d+)\s*x", expand=False)
                        .astype(float, errors="ignore")
                        .astype("Int64", errors="ignore")
                    )

            # Extract GPU RAM
                    df_b["GPU RAM"] = df_b["GPU Model"].str.extract(r"(\d+\s*GB)", expand=False)

            # Simplify GPU Model
                    df_b["GPU Model"] = df_b["GPU Model"].str.extract(
                        r"(H100 HGX Cluster|L40S Cluster|Baremetal.*?HGX|Baremetal.*?L40S|Bare Metal L40S|H100|L40S)", expand=False
                    )
                    df_b["GPU Model"] = df_b["GPU Model"].str.replace(r"\d+\s*x\s*", "", regex=True)

        # Reset index and clean data
                df_b = df_b.drop_duplicates(subset=["GPU Model"]).reset_index(drop=True)
                df_b["Price"] = df_b["Price"].replace({'\$': '', ',': ''}, regex=True).astype(float, errors="ignore")
                df_b['Price'] = df_b['Price'].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "")
                df_b["Source"] = "Shakti Cloud"
                df_b = df_b[["GPU Model", "GPU Count", "Price", "GPU RAM", "Source"]]
                combined_df = pd.concat([combined_df, df_b], ignore_index=True)


    # Replicate Pricing Data
    replicate_data = scrape_replicate_pricing()
    if replicate_data:
        df2_r = save_to_dataframe(replicate_data)
        df3_r = df2_r[df2_r["Hardware Name"].str.contains("NVIDIA H100|NVIDIA L40S", case=False, na=False)]
        df3_r = df3_r[["Hardware Name", "GPU Quantity", "Per-Hour Price", "GPU RAM"]]
        df3_r.rename(columns={
            "Hardware Name": "GPU Model",
            "GPU Quantity": "GPU Count",
            "Per-Hour Price": "Price"
        }, inplace=True)

        # Update GPU Count extraction to handle invalid or varying cases
        # Extract valid numeric GPU Count values and handle invalid/missing entries
        df3_r['GPU Count'] = df3_r['GPU Count'].str.extract(r'^(\d+)x$')  # Extract numeric values with "x" at the end
        df3_r['GPU Count'] = pd.to_numeric(df3_r['GPU Count'], errors='coerce')  # Convert to int or NaN


        df3_r = df3_r.reset_index(drop=True)
        df3_r['GPU Model'] = df3_r['GPU Model'].str.replace(r'^\d+x\s*', '', regex=True)
        df3_r['GPU Model'] = df3_r['GPU Model'].str.replace(r'\bGPU\b', '', regex=True).str.strip()
        df3_r = df3_r[["GPU Model", "GPU Count", "Price", "GPU RAM"]]
        df3_r['Price'] = df3_r['Price'].astype(str).str.replace('[^\d.]', '', regex=True)
        df3_r['Price'] = pd.to_numeric(df3_r['Price'], errors='coerce')
        df3_r['Price'] = df3_r['Price'].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "")

        df3_r['Source'] = 'Replicate'  # Add source column
        combined_df = pd.concat([combined_df, df3_r], ignore_index=True)
         # Add Node column based on GPU count and model

    together_ai_data = scrape_together_ai_pricing()
    if together_ai_data:
       # Create DataFrame
        df = pd.DataFrame(together_ai_data, columns=['Hardware', 'Price'])

# Filter the DataFrame
        df_t = df[df['Hardware'].str.contains('H100|L40S')]

# Split the Hardware column
        df_t[['GPU Count', 'GPU Model', 'GPU RAM']] = df_t['Hardware'].str.extract(r'(\d+)x\s(.+?)\s(\d+GB)')

# Update GPU Model column with full names
        df_t['GPU Model'] = df_t['GPU Model'].replace({
            'L40S': 'Nvidia L40S',
            'H100': 'Nvidia H100'
        })

# Convert Price from per minute to per hour
        df_t['Price'] = df_t['Price'].str.replace('$', '', regex=False).astype(float) * 60
        df_t['Price'] = df_t['Price'].map('${:,.2f}'.format)  # Format as currency

# Add the Source column
        df_t['Source'] = 'together.ai'

# Rearrange columns for the requested order
        df_t = df_t[['GPU Model', 'GPU Count', 'Price', 'GPU RAM', 'Source']]

# Reset the index
        df_t = df_t.reset_index(drop=True)

# Display the final DataFrame


        combined_df = pd.concat([combined_df, df_t], ignore_index=True)


    digitalo_data =scrape_digitalocean_gpu_pricing()
    if digitalo_data:
        df_d = pd.DataFrame(digitalo_data)

        # Remove rows where any of the key columns (Price, GPU RAM) have "N/A"
        df_d = df_d[~df_d[['Price', 'GPU RAM']].isin(['N/A']).any(axis=1)].reset_index(drop=True)

        # Keep only the required columns
        df_d = df_d[["GPU Model", "GPU Count", "Price", "GPU RAM", "Source"]]
        combined_df = pd.concat([combined_df, df_d], ignore_index=True)

 
# Scrape GPU pricing from DigitalOcean
    gpu = scrape_runpod_gpu_pricing()  # Function must be defined elsewhere
    if gpu:
        df = pd.DataFrame(gpu, columns=['GPU Model', 'GPU Count', 'GPU RAM', 'Price'])

# Ensure GPU Count is integer type
        df['GPU Count'] = df['GPU Count'].astype(int)

# Rename GPU Models
        df['GPU Model'] = df['GPU Model'].replace({'H100 SXM': 'Nvidia H100', 'L40S': 'Nvidia L40S'})

# Trim extra spaces from the GPU Model column
        df['GPU Model'] = df['GPU Model'].str.strip()

# Filter rows where 'GPU Model' contains "H100" or "L40S"
        filtered_df = df[df['GPU Model'].str.contains('H100|L40S', case=False, na=False)]

# Reset the index
        filtered_df.reset_index(drop=True, inplace=True)
        filtered_df["Source"] = "runpod"
        filtered_df = filtered_df[["GPU Model", "GPU Count", "Price", "GPU RAM", "Source"]]


        combined_df = pd.concat([combined_df, filtered_df], ignore_index=True)


    nebius_data =scrape_nebius_gpu_pricing()
    if nebius_data:
        df_n = pd.DataFrame(nebius_data, columns=['GPU Model', 'GPU Count', 'Price', 'GPU RAM', 'Source'])
        combined_df = pd.concat([combined_df, df_n], ignore_index=True)


    combined_df = add_node_column(combined_df)

    if not combined_df.empty:
        
        st.dataframe(combined_df, use_container_width=True)  # ✅ Show all columns
    else:
        st.write("⚠️ No data to display from any source.")



# Assuming combined_df is your DataFrame containing GPU data

st.sidebar.header("🔎 Filter Results")

input_gpu_name = st.sidebar.text_input("Enter GPU Model (e.g., Nvidia H100, L40S)").strip()
input_gpu_count = st.sidebar.text_input("Enter GPU Count (leave blank to skip)").strip()
input_gpu_count = int(input_gpu_count) if input_gpu_count.isdigit() else None
input_node = st.sidebar.text_input("Enter Node Info (leave blank to skip)").strip()

# 🔹 **Ensure Main() Runs Before Using Data**
if __name__ == "__main__":
    main()  # ✅ Run main() before filtering

    if 'combined_df' in globals() and not combined_df.empty:
        if input_gpu_name:
            result = filter_gpu_data(combined_df, input_gpu_name, input_gpu_count, input_node)

            if not result.empty:
                result.insert(0, 'Sequence', range(1, len(result) + 1))
                st.subheader("📊 Filtered Results")
                st.dataframe(result.reset_index(drop=True), use_container_width=True)
            else:
                st.write(f"❌ No data found for **GPU Model: {input_gpu_name}**, **GPU Count: {input_gpu_count}**, **Node: {input_node}**.")
    else:
        st.write("⚠️ Error: GPU data has not been loaded. Please check if `main()` has run correctly.")
