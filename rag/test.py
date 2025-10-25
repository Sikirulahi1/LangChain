import httpx
import asyncio

async def send_summarization_request():
    url = "https://ai-sodc.optimusai.ai/ai/summarize"
    
    payload = {
        "text": "Dental plaque is far more complex than the fuzzy film you may feel on your teeth. This biofilm begins forming within hours after brushing as proteins from saliva adhere to the tooth surface, creating what's called a pellicle. Bacteria then attach to this sticky foundation and multiply rapidly. Within 48 hours, this bacterial colony organizes into a structured community with different species performing specific functions. The outer layers contain aerobic bacteria that can survive in oxygen, while deeper layers harbor anaerobic bacteria that thrive without it. These microorganisms feed on carbohydrates from your diet and produce acids as waste products. These acids gradually demineralize tooth enamel by pulling out calcium and phosphate minerals, eventually creating a cavity if left unchecked. What makes plaque particularly problematic is its protective matrix - a slimy substance secreted by bacteria that shields them from saliva, oxygen, and even antimicrobial agents in toothpaste. This is why mechanical removal through brushing and flossing is essential - chemical agents alone often can't penetrate this biofilm effectively. The longer plaque remains undisturbed, the more it hardens into calculus (tartar), which cannot be removed by brushing alone and creates rough surfaces where even more plaque can accumulate. This cycle leads to not only tooth decay but also gingival inflammation as bacterial toxins irritate gum tissues. Understanding that plaque is a living, organized ecosystem rather than just \"dirty teeth\" helps explain why consistent daily disruption of this biofilm is crucial for maintaining oral health and preventing both cavities and gum disease"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            print(result)
            return result
    except httpx.RequestError as exc:
        print(f"Request error: {exc}")
        return None
    except httpx.HTTPStatusError as exc:
        print(f"HTTP status error: {exc.response.status_code} - {exc}")
        return None

# Run the request
result = asyncio.run(send_summarization_request())
if result:
    print(f"Success: {result}")