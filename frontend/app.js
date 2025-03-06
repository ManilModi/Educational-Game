document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('gemini-form');
    const responseDiv = document.getElementById('response');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const symbol = document.getElementById('symbol').value;
        getGeminiPrice(symbol);
    });

    function getGeminiPrice(symbol) {
        fetch(`/api/gemini/price/${symbol}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    responseDiv.innerHTML = `<p>Error: ${data.error}</p>`;
                } else {
                    responseDiv.innerHTML = `<p>The current price of ${data.symbol} is ${data.price}</p>`;
                }
            })
            .catch(error => {
                responseDiv.innerHTML = `<p>Error: ${error.message}</p>`;
            });
    }
});
