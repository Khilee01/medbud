import requests

def get_medication_info(medication_name):
    """
    Get medication information from FDA API.
    Returns a dictionary with medication info or None if not found.
    """
    try:
        # FDA API endpoint for drug information
        url = f"https://api.fda.gov/drug/label.json?search=openfda.brand_name:{medication_name}&limit=1"
        
        response = requests.get(url)
        data = response.json()
        
        if 'results' in data and len(data['results']) > 0:
            result = data['results'][0]
            
            # Extract dosage information
            dosage = "Not specified"
            if 'dosage_and_administration' in result:
                dosage = result['dosage_and_administration'][0]
            
            return {
                'name': medication_name,
                'dosage': dosage,
                'source': 'US FDA'
            }
        else:
            print(f"No information found for '{medication_name}' in FDA database.")
            return None
            
    except Exception as e:
        print(f"FDA API error: {e}")
        return None
