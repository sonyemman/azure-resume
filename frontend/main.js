window.addEventListener("DOMContentLoaded", (event) => {
    getVisitorCount();
})

const functionApi = 'http://localhost:7071/api/http_trigger';

const getVisitorCount = () => {
    let count = 30 
    fetch(functionApi).then(response => {
        return response.json()
    }).then(response => {
        console.log("Website called funciton API");
        count = response.count; 
        document.getElementById("counter").innerText = count; 
    }).catch(function(error){
        console.log(error); 
    });

    return count
}

