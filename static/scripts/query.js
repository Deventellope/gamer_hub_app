// handles all logic pertaining to user game search request
async function  query_request_handler(event){

    const clicked_button= event.target
    // disable clicked button
    clicked_button.disabled= true
    // get query value
    const input_element= "cliked input element"

    usesr_query_input= input_element.value

    const user_query= await fetch("endpoint", {
        method: POST,
        // contenypeo: POST,
        headers: POST,
        body: JSON.stringify({ "user_query": user_query })
    })
}