const fetchGitHubStats = require("./utils/fetchGithubStats");
const generateGitHubStatsImage = require("./GenerateGithubStatsImage");
const generateLanguageChart = require("./GenerateMostUsedLanguages");
const { calculateScore, getGrade } = require("./utils/calculateGrade");

async function main() {
    console.log("🚀 Generando estadísticas de GitHub...");

    const stats = await fetchGitHubStats();

    if (!stats) {
        console.error("❌ No se pudieron obtener las estadísticas de GitHub.");
        process.exit(1);
    }

    const score = calculateScore(stats);
    const grade = getGrade(score);

    await generateGitHubStatsImage(stats, grade);
    generateLanguageChart(stats.languages || []);

    console.log("✅ Imágenes de estadísticas y lenguajes generadas correctamente.");
}

main().catch((error) => {
    console.error("❌ Error inesperado generando las estadísticas:", error);
    process.exit(1);
});
