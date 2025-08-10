document.addEventListener('DOMContentLoaded', function() {
    const username = 'JoaoKraideM'; // Seu username do GitHub
    const gridContainer = document.getElementById('contributions-grid');
    const countElement = document.getElementById('contributions-count');
    
    // Cores de intensidade (0-4)
    const intensityColors = ['#ebedf0', '#9be9a8', '#40c463', '#30a14e', '#216e39'];
    
    // Função para determinar a intensidade
    function getIntensity(count) {
        if (count === 0) return 0;
        if (count <= 9) return 1;
        if (count <= 19) return 2;
        if (count <= 29) return 3;
        return 4;
    }
    
    // Função para gerar dados simulados (apenas para teste)
    function generateSimulatedData() {
        const today = new Date();
        const contributions = [];
        let total = 0;
        
        // Gera dados para os últimos 371 dias (53 semanas)
        for (let i = 0; i < 371; i++) {
            const date = new Date(today);
            date.setDate(date.getDate() - i);
            
            // Simula mais atividade durante a semana
            const dayOfWeek = date.getDay();
            const count = dayOfWeek === 0 || dayOfWeek === 6 
                ? Math.floor(Math.random() * 3)  // Menos nos fins de semana
                : Math.floor(Math.random() * 10); // Mais durante a semana
            
            total += count;
            
            contributions.push({
                date: date.toISOString().split('T')[0],
                count: count,
                intensity: getIntensity(count)
            });
        }
        
        return {
            total: total,
            contributions: contributions.reverse() // Do mais antigo para o mais novo
        };
    }
    
    // Função para renderizar o gráfico
    function renderGraph(data) {
        gridContainer.innerHTML = '';
        
        // Atualiza o contador
        countElement.textContent = `${data.total} contribuições em ${new Date().getFullYear()}`;
        
        // Adiciona as células ao grid
        data.contributions.forEach(day => {
            const cell = document.createElement('div');
            cell.className = 'contribution-cell';
            cell.style.backgroundColor = intensityColors[day.intensity];
            cell.setAttribute('data-intensity', day.intensity);
            gridContainer.appendChild(cell);
        });
    }
    
    // Para usar dados reais, substitua por:    
    fetch(`/api/github-contributions?username=${username}`)
        .then(response => response.json())
        .then(renderGraph)
        .catch(() => renderGraph(generateSimulatedData()));
}); 