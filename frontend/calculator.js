/**
 * FarmGuard AI - PrithviBio Calculation Engine
 * Lightweight carbon credit calculator for farmers
 */

// Crop data with realistic values
const cropDatabase = {
    tomato: {
        name: "Tomatoes",
        pricePerKg: 30,
        yieldPerAcreKg: 2000,
        revenuePerAcre: 60000,
        emoji: "🍅"
    },
    rice: {
        name: "Rice",
        pricePerKg: 25,
        yieldPerAcreKg: 2500,
        revenuePerAcre: 62500,
        emoji: "🌾"
    },
    wheat: {
        name: "Wheat",
        pricePerKg: 28,
        yieldPerAcreKg: 2200,
        revenuePerAcre: 61600,
        emoji: "🌾"
    },
    maize: {
        name: "Maize",
        pricePerKg: 22,
        yieldPerAcreKg: 3000,
        revenuePerAcre: 66000,
        emoji: "🌽"
    },
    cotton: {
        name: "Cotton",
        pricePerKg: 65,
        yieldPerAcreKg: 800,
        revenuePerAcre: 52000,
        emoji: "🪡"
    },
    vegetables: {
        name: "Mixed Vegetables",
        pricePerKg: 35,
        yieldPerAcreKg: 1800,
        revenuePerAcre: 63000,
        emoji: "🥬"
    }
};

/**
 * Main calculation function for PrithviBio benefits
 * 
 * @param {number} acres - Farm size in acres
 * @param {string} cropType - Crop type key (tomato, rice, wheat, etc.)
 * @returns {object} Benefits including yield boost, carbon credits, and revenue
 */
function calculateFarmBenefits(acres, cropType) {
    // PrithviBio scientific data:
    // - 15% average yield increase (based on Chlorella studies)
    // - 2.5 carbon credits per acre per year
    // - Each credit = 1 metric ton CO₂ equivalent
    
    const YIELD_INCREASE_PERCENT = 15;
    const CARBON_CREDITS_PER_ACRE = 2.5;
    const PRICE_PER_CREDIT_USD = 15; // $15 per credit (global market average)
    const USD_TO_INR = 83;
    
    const crop = cropDatabase[cropType];
    
    if (!crop) {
        return {
            error: "Invalid crop type selected"
        };
    }
    
    // Calculate current revenue
    const currentRevenue = acres * crop.revenuePerAcre;
    
    // Calculate extra crop revenue from yield increase
    const extraCropRevenue = currentRevenue * (YIELD_INCREASE_PERCENT / 100);
    
    // Calculate carbon credits
    const totalCarbonCredits = acres * CARBON_CREDITS_PER_ACRE;
    const carbonRevenueUSD = totalCarbonCredits * PRICE_PER_CREDIT_USD;
    const carbonRevenueINR = carbonRevenueUSD * USD_TO_INR;
    
    // Calculate total benefits
    const totalBonusINR = extraCropRevenue + carbonRevenueINR;
    const totalBonusUSD = totalBonusINR / USD_TO_INR;
    
    // Calculate CO₂ sequestered (kg)
    const co2SequesteredKg = totalCarbonCredits * 1000;
    
    // Calculate trees equivalent (1 tree absorbs ~22.5 kg CO₂/year)
    const treesEquivalent = Math.round(co2SequesteredKg / 22.5);
    
    return {
        // Basic info
        acres: acres,
        cropName: crop.name,
        cropEmoji: crop.emoji,
        
        // Yield stats
        yieldIncreasePercent: YIELD_INCREASE_PERCENT,
        currentRevenueINR: Math.round(currentRevenue),
        extraCropRevenueINR: Math.round(extraCropRevenue),
        
        // Carbon credit stats
        carbonCredits: totalCarbonCredits.toFixed(1),
        carbonRevenueINR: Math.round(carbonRevenueINR),
        carbonRevenueUSD: carbonRevenueUSD.toFixed(2),
        
        // Environmental impact
        co2SequesteredKg: Math.round(co2SequesteredKg),
        treesEquivalent: treesEquivalent,
        
        // Total financial gain
        totalBonusINR: Math.round(totalBonusINR),
        totalBonusUSD: totalBonusUSD.toFixed(2),
        
        // Formatted strings for display
        formattedYieldBoost: `+${YIELD_INCREASE_PERCENT}%`,
        formattedExtraCropIncome: `₹${Math.round(extraCropRevenue).toLocaleString()}`,
        formattedCarbonCredits: `${totalCarbonCredits.toFixed(1)} Credits`,
        formattedCarbonValue: `₹${Math.round(carbonRevenueINR).toLocaleString()}`,
        formattedTotalBonus: `₹${Math.round(totalBonusINR).toLocaleString()}`,
        formattedCO2Removed: `${Math.round(co2SequesteredKg).toLocaleString()} kg`,
        formattedTreesEquivalent: `${treesEquivalent.toLocaleString()} trees`,
        
        // Message for farmer
        message: `🌱 With PrithviBio on ${acres} acre(s) of ${crop.name}, you'll earn ₹${Math.round(totalBonusINR).toLocaleString()} extra per year!`
    };
}

/**
 * Calculate benefits for multiple years
 */
function calculateMultiYearBenefits(acres, cropType, years) {
    const yearlyResults = [];
    let cumulativeCredits = 0;
    let cumulativeRevenue = 0;
    
    for (let i = 1; i <= years; i++) {
        const result = calculateFarmBenefits(acres, cropType);
        cumulativeCredits += parseFloat(result.carbonCredits);
        cumulativeRevenue += result.totalBonusINR;
        yearlyResults.push({
            year: i,
            credits: result.carbonCredits,
            revenue: result.totalBonusINR
        });
    }
    
    return {
        years: years,
        yearlyBreakdown: yearlyResults,
        totalCredits: cumulativeCredits.toFixed(1),
        totalRevenueINR: Math.round(cumulativeRevenue),
        message: `💰 Over ${years} years, you'll earn ₹${Math.round(cumulativeRevenue).toLocaleString()} from PrithviBio!`
    };
}

/**
 * Compare PrithviBio vs Chemical Fertilizers
 */
function compareWithChemicalFertilizers(acres) {
    const chemicalCostPerAcre = 5000; // ₹5,000 per acre for chemical fertilizers
    const prithviBioCostPerAcre = 1500; // ₹1,500 per acre for PrithviBio
    
    const chemicalTotalCost = acres * chemicalCostPerAcre;
    const prithviBioTotalCost = acres * prithviBioCostPerAcre;
    
    // Calculate extra benefits from PrithviBio
    const benefits = calculateFarmBenefits(acres, "vegetables");
    
    const savings = chemicalTotalCost - prithviBioTotalCost;
    const totalAdvantage = benefits.totalBonusINR + savings;
    
    return {
        chemicalFertilizerCost: chemicalTotalCost,
        prithviBioCost: prithviBioTotalCost,
        costSavings: savings,
        carbonRevenue: benefits.carbonRevenueINR,
        cropRevenueBonus: benefits.extraCropRevenueINR,
        totalAdvantage: totalAdvantage,
        message: `💚 Switch to PrithviBio and save ₹${savings.toLocaleString()} on fertilizers, plus earn ₹${benefits.totalBonusINR.toLocaleString()} in carbon credits and extra yield!`
    };
}

// Export for use in HTML
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { calculateFarmBenefits, calculateMultiYearBenefits, compareWithChemicalFertilizers, cropDatabase };
}