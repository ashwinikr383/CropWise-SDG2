"""
CropWise - Comprehensive Crop Information Repository
SDG 2: Zero Hunger | Sustainable Precision Agriculture

Provides agricultural profiles, nutritional values, growing requirements,
and SDG 2 food security relevance for all 22 supported crops.
"""

CROP_DETAILS = {
    "rice": {
        "scientific_name": "Oryza sativa",
        "category": "Cereal Grain / Staple",
        "season": "Kharif (Monsoon)",
        "duration": "100 - 150 days",
        "soil_type": "Clayey or heavy loam with high water-retention capacity",
        "water_req": "High (Standing water during vegetative phase, 1200-2000 mm total)",
        "sdg2_impact": "Primary caloric staple for over 50% of the world's population, vital for combating global hunger.",
        "nutrition": "Rich in complex carbohydrates, protein (approx 7%), B-vitamins (thiamine, niacin), and iron.",
        "icon": "🌾",
        "description": "Rice is the cornerstone of global food security. It thrives in flooded paddy soils with high temperatures and prolonged humidity."
    },
    "maize": {
        "scientific_name": "Zea mays",
        "category": "Cereal Grain / Coarse Grain",
        "season": "Kharif & Rabi",
        "duration": "90 - 120 days",
        "soil_type": "Well-drained deep loamy soil rich in organic matter",
        "water_req": "Moderate (500 - 800 mm evenly distributed)",
        "sdg2_impact": "Versatile staple food and livestock feed essential for protein security and bio-economy.",
        "nutrition": "High in dietary fiber, carotenoids (lutein, zeaxanthin), phosphorus, and magnesium.",
        "icon": "🌽",
        "description": "Maize is exceptionally efficient in carbon fixation (C4 plant). Requires adequate nitrogen and moderate moisture."
    },
    "chickpea": {
        "scientific_name": "Cicer arietinum",
        "category": "Legume / Pulse",
        "season": "Rabi (Winter/Dry)",
        "duration": "90 - 120 days",
        "soil_type": "Well-drained sandy loam or clay loam (pH 6.0 - 8.0)",
        "water_req": "Low (Drought-tolerant, 300 - 450 mm)",
        "sdg2_impact": "Affordable plant protein source for vulnerable communities; fixes atmospheric nitrogen to regenerate soil fertility.",
        "nutrition": "High protein (20-22%), soluble fiber, folate, iron, and zinc.",
        "icon": "🧆",
        "description": "Chickpea is a climate-resilient dryland pulse. Thrives in cool weather and requires high potassium for drought tolerance."
    },
    "kidney beans": {
        "scientific_name": "Phaseolus vulgaris",
        "category": "Legume / Pulse",
        "season": "Kharif / Spring",
        "duration": "90 - 130 days",
        "soil_type": "Deep, loose, fertile soil with moderate acidity (pH 5.5 - 6.5)",
        "water_req": "Moderate (400 - 600 mm)",
        "sdg2_impact": "High-density nutrient profile providing key micronutrients to prevent malnutrition and stunting.",
        "nutrition": "Dense source of plant protein, dietary fiber, molybdenum, iron, and potassium.",
        "icon": "🫘",
        "description": "Commonly known as Rajma. Sensitive to extreme heat and waterlogging; performs best in temperate and subtropical hills."
    },
    "pigeon peas": {
        "scientific_name": "Cajanus cajan",
        "category": "Legume / Pulse",
        "season": "Kharif (Semi-arid)",
        "duration": "140 - 240 days",
        "soil_type": "Deep loam or black cotton soil with good drainage",
        "water_req": "Low to Moderate (Drought-hardy deep root system)",
        "sdg2_impact": "Key protein source in tropical drylands; excellent intercrop for soil conservation and erosion prevention.",
        "nutrition": "Protein (approx 21%), essential amino acids (methionine, lysine), and B-complex vitamins.",
        "icon": "🌱",
        "description": "Pigeon pea (Arhar/Tur) is a deeply rooted drought-hardy legume capable of extracting moisture from subsoil horizons."
    },
    "moth beans": {
        "scientific_name": "Vigna aconitifolia",
        "category": "Legume / Arid Pulse",
        "season": "Kharif (Arid)",
        "duration": "75 - 90 days",
        "soil_type": "Sandy to light sandy loam, tolerates wide pH variation",
        "water_req": "Very Low (200 - 350 mm, ultra-drought resistant)",
        "sdg2_impact": "Critical lifeline for food security in hyper-arid desert regions where most crops fail completely.",
        "nutrition": "Rich in protein (22-24%), calcium, zinc, and dietary fiber.",
        "icon": "🌿",
        "description": "One of the most drought-hardy legumes on Earth. Spreads as ground cover, reducing soil erosion during sandstorms."
    },
    "mung bean": {
        "scientific_name": "Vigna radiata",
        "category": "Legume / Pulse",
        "season": "Summer & Kharif",
        "duration": "60 - 75 days",
        "soil_type": "Well-drained fertile loam with neutral to slightly acidic pH",
        "water_req": "Low to Moderate (350 - 500 mm)",
        "sdg2_impact": "Short-duration cash and protein crop that fits easily between cereal cropping cycles.",
        "nutrition": "Easily digestible protein (24%), rich in antioxidants (vitexin), potassium, and folate.",
        "icon": "🟢",
        "description": "Green gram is an ultra-fast maturing pulse that improves soil organic matter and provides rapid emergency income."
    },
    "black gram": {
        "scientific_name": "Vigna mungo",
        "category": "Legume / Pulse",
        "season": "Kharif & Summer",
        "duration": "75 - 90 days",
        "soil_type": "Heavier soils, loams, and black cotton soils",
        "water_req": "Moderate (400 - 600 mm)",
        "sdg2_impact": "High-value pulse widely utilized across South Asia for fermented nutritious staple preparations.",
        "nutrition": "Very high iron content, protein (24-26%), calcium, and phosphorus.",
        "icon": "🔘",
        "description": "Urad dal thrives in warm, humid conditions. Notable for soil nitrogen enrichment and tolerance to warm nights."
    },
    "lentil": {
        "scientific_name": "Lens culinaris",
        "category": "Legume / Pulse",
        "season": "Rabi (Cool Season)",
        "duration": "100 - 130 days",
        "soil_type": "Light loams to clay soils with good aeration",
        "water_req": "Low (300 - 450 mm)",
        "sdg2_impact": "Ancient crop that provides essential dietary amino acids and requires minimal synthetic fertilizer.",
        "nutrition": "Abundant protein (25%), polyphenol antioxidants, non-heme iron, and prebiotics.",
        "icon": "🥣",
        "description": "Lentils perform best in cool growing seasons with modest moisture. Sensitive to water stagnation and high humidity during maturity."
    },
    "pomegranate": {
        "scientific_name": "Punica granatum",
        "category": "Fruit / Horticultural Tree",
        "season": "Perennial (All-year flowering flushes)",
        "duration": "5 - 7 months fruit development",
        "soil_type": "Deep loamy or alluvial soil, tolerates salinity and caliche",
        "water_req": "Low to Moderate (Drip irrigation recommended)",
        "sdg2_impact": "High-income horticultural crop supporting smallholder livelihood resilience and micro-nutrient diversity.",
        "nutrition": "Potent antioxidants (punicalagins, anthocyanins), Vitamin C, and dietary fiber.",
        "icon": "🍎",
        "description": "Pomegranate thrives in hot, dry summers and mild winters. Requires dry weather during fruit ripening to prevent fruit cracking."
    },
    "banana": {
        "scientific_name": "Musa acuminata",
        "category": "Fruit / Commercial Perennial",
        "season": "Year-round in humid tropics",
        "duration": "10 - 14 months to harvest",
        "soil_type": "Deep, rich, well-drained fertile loam with high organic matter",
        "water_req": "High (1500 - 2500 mm or constant scheduled irrigation)",
        "sdg2_impact": "Major global source of dietary energy, accessible fruit calories, and rural agricultural employment.",
        "nutrition": "High potassium, Vitamin B6, Vitamin C, and quickly available energy carbohydrates.",
        "icon": "🍌",
        "description": "A heavy feeder of Nitrogen and Potassium. Demands abundant soil moisture, high humidity, and protection from severe winds."
    },
    "mango": {
        "scientific_name": "Mangifera indica",
        "category": "Fruit / Orchard Tree",
        "season": "Summer (flowering in winter)",
        "duration": "Perennial (fruits 4-5 months post-bloom)",
        "soil_type": "Deep, well-drained alluvial, loam, or red soil (pH 5.5 - 7.5)",
        "water_req": "Moderate (Requires dry spell for flowering, 750 - 1200 mm)",
        "sdg2_impact": "The 'King of Fruits' provides essential Vitamin A to mitigate childhood vision disorders in developing regions.",
        "nutrition": "Exceptionally high in beta-carotene (provitamin A), Vitamin C, folate, and pectin.",
        "icon": "🥭",
        "description": "Requires frost-free tropical to subtropical conditions. A distinct dry season prior to flowering is critical for abundant fruit set."
    },
    "grapes": {
        "scientific_name": "Vitis vinifera",
        "category": "Fruit / Vineyard Horticultural",
        "season": "Perennial (Spring-Summer flush)",
        "duration": "120 - 150 days per fruiting cycle",
        "soil_type": "Well-drained gravelly or sandy loam with good aeration",
        "water_req": "Moderate (500 - 700 mm, drip managed)",
        "sdg2_impact": "High-value export cash crop providing substantial economic empowerment for rural farm households.",
        "nutrition": "Resveratrol, flavonoids, potassium, Vitamin K, and natural simple carbohydrates.",
        "icon": "🍇",
        "description": "Vines demand high Potassium and Phosphorus levels. Needs warm dry sunny weather during ripening to maximize sugars."
    },
    "watermelon": {
        "scientific_name": "Citrullus lanatus",
        "category": "Fruit / Cucurbit",
        "season": "Zaid / Summer",
        "duration": "80 - 100 days",
        "soil_type": "Sandy loam or riverbed alluvium with excellent drainage",
        "water_req": "Moderate (400 - 600 mm, dry atmosphere needed)",
        "sdg2_impact": "Crucial summer hydration and electrolyte source in arid and semi-arid agro-ecological zones.",
        "nutrition": "Over 91% water, packed with lycopene, citrulline, and Vitamin A.",
        "icon": "🍉",
        "description": "Warm-season crop that thrives in long sunny days with warm nights. Susceptible to fungal blight in continuous rain."
    },
    "muskmelon": {
        "scientific_name": "Cucumis melo",
        "category": "Fruit / Cucurbit",
        "season": "Summer / Zaid",
        "duration": "70 - 90 days",
        "soil_type": "Light, sandy or well-drained fertile loam (pH 6.0 - 7.0)",
        "water_req": "Low to Moderate (Minimal rain during sweetening phase)",
        "sdg2_impact": "Rapid-turnaround cash crop providing nutrient-dense hydration during dry seasonal hunger gaps.",
        "nutrition": "Extremely high in Vitamin A, Vitamin C, carotenoids, and potassium.",
        "icon": "🍈",
        "description": "Demands hot, dry climates with abundant sunshine during ripening. Excess rain or humidity diminishes sugar concentration."
    },
    "apple": {
        "scientific_name": "Malus domestica",
        "category": "Fruit / Temperate Orchard",
        "season": "Temperate Autumn harvest",
        "duration": "Perennial (130 - 150 days post blossom)",
        "soil_type": "Deep, well-drained loamy soil with high organic matter (pH 5.5 - 6.5)",
        "water_req": "Moderate to High (1000 - 1250 mm distributed)",
        "sdg2_impact": "Foundational temperate fruit supporting hill agriculture economies and widespread dietary quality.",
        "nutrition": "Soluble dietary fiber (pectin), quercetin, polyphenols, and Vitamin C.",
        "icon": "🍏",
        "description": "Requires chilling hours (<7°C for 800-1200 hrs) to break winter dormancy. Demands significant potassium and phosphorus."
    },
    "orange": {
        "scientific_name": "Citrus sinensis",
        "category": "Fruit / Citrus Orchard",
        "season": "Winter - Spring harvest",
        "duration": "Perennial (8 - 10 months to maturity)",
        "soil_type": "Well-aerated sandy loam or light clay with no waterlogging",
        "water_req": "Moderate (900 - 1200 mm)",
        "sdg2_impact": "Essential citrus fruit combatting scurvy, micronutrient deficiencies, and promoting immune resilience.",
        "nutrition": "High concentration of ascorbic acid (Vitamin C), bioflavonoids, potassium, and folate.",
        "icon": "🍊",
        "description": "Performs well in subtropical conditions. Requires dry weather during flowering and moderate moisture during fruit sizing."
    },
    "papaya": {
        "scientific_name": "Carica papaya",
        "category": "Fruit / Semi-Perennial",
        "season": "Year-round tropical",
        "duration": "9 - 11 months from planting to first harvest",
        "soil_type": "Rich sandy loam with excellent drainage (intolerant of waterlogging)",
        "water_req": "Moderate to High (1200 - 1600 mm)",
        "sdg2_impact": "Fast-bearing fruit delivering year-round micronutrients to vulnerable rural families.",
        "nutrition": "Enzyme papain, provitamin A carotenoids, Vitamin C, and digestive enzymes.",
        "icon": "🥭",
        "description": "Ultra-sensitive to root rot in poorly drained soil. Thrives in warm, sunny tropical climates with steady moisture."
    },
    "coconut": {
        "scientific_name": "Cocos nucifera",
        "category": "Plantation / Multi-purpose Palm",
        "season": "Continuous year-round harvest",
        "duration": "Perennial (5-6 years to first yield, productive for 60+ years)",
        "soil_type": "Coastal sandy loam, alluvial, or lateritic soils with good aeration",
        "water_req": "High (1500 - 2500 mm or constant coastal water table)",
        "sdg2_impact": "The 'Tree of Life' provides food, cooking oil, hydration, building materials, and income for coastal communities.",
        "nutrition": "Medium-chain triglycerides (lauric acid), minerals (manganese, copper), and electrolyte-rich water.",
        "icon": "🥥",
        "description": "Ideal for warm, humid coastal zones. Requires high atmospheric humidity and cannot tolerate frost or waterlogging."
    },
    "cotton": {
        "scientific_name": "Gossypium hirsutum",
        "category": "Fiber / Cash Crop",
        "season": "Kharif (Warm season)",
        "duration": "150 - 180 days",
        "soil_type": "Deep black cotton soils (Vertisols) or fertile loams",
        "water_req": "Moderate (700 - 1000 mm)",
        "sdg2_impact": "Primary industrial cash crop generating rural employment and household income needed to purchase food.",
        "nutrition": "Non-edible fiber; cottonseed oil provides edible fat and protein-rich cake for dairy livestock.",
        "icon": "🧵",
        "description": "White Gold demands warm temperatures throughout vegetative development and clear sunny weather during boll opening."
    },
    "jute": {
        "scientific_name": "Corchorus olitorius",
        "category": "Fiber / Commercial Crop",
        "season": "Monsoon / Kharif",
        "duration": "120 - 150 days",
        "soil_type": "Alluvial, river delta soils, sandy to clayey loam",
        "water_req": "High (1500 - 1800 mm, standing water tolerant)",
        "sdg2_impact": "Biodegradable natural fiber supporting smallholder delta economies and sustainable food packaging solutions.",
        "nutrition": "Fiber crop; young tender leaves are consumed as nutrient-dense leafy greens in many riverine communities.",
        "icon": "🌾",
        "description": "Thrives in warm, humid tropical climates with frequent monsoon rains. Requires warm temperatures and fertile river silt."
    },
    "coffee": {
        "scientific_name": "Coffea arabica / canephora",
        "category": "Beverage / Plantation Cash Crop",
        "season": "Winter / Spring harvest",
        "duration": "Perennial (3-4 years to first crop, 7-9 months bean ripening)",
        "soil_type": "Deep, volcanic, porous, fertile soils rich in humus (pH 5.5 - 6.5)",
        "water_req": "Moderate to High (1500 - 2200 mm with dry spell for flowering)",
        "sdg2_impact": "Key export commodity providing millions of smallholder families worldwide with crucial agricultural livelihoods.",
        "nutrition": "Rich in chlorogenic acid antioxidants and caffeine.",
        "icon": "☕",
        "description": "Prefers shaded hill slopes, moderate temperatures, and high rainfall followed by a dry period to stimulate flowering."
    }
}


def get_crop_info(crop_name: str) -> dict:
    """Retrieve detailed information dictionary for a given crop."""
    crop_name_lower = crop_name.strip().lower()
    return CROP_DETAILS.get(
        crop_name_lower,
        {
            "scientific_name": "Plantae",
            "category": "Agricultural Crop",
            "season": "Variable",
            "duration": "90 - 150 days",
            "soil_type": "Fertile loam with balanced organic content",
            "water_req": "Moderate (600 - 1000 mm)",
            "sdg2_impact": "Supports household food security and regional agricultural resilience.",
            "nutrition": "Essential dietary energy and micronutrients.",
            "icon": "🌱",
            "description": f"{crop_name.capitalize()} is an important agricultural crop suited to specific soil and weather conditions."
        }
    )
