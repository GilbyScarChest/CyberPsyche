

var comment = document.querySelectorAll(".comment");
var msg_list = []



// function postComment() {

//     // let $jq = jQuery.noConflict();

//     let content = document.getElementById("content").value;
//     // let content = d3.select("#content").text()

//     // let commentPage = d3.select("#comment-page").append("div")
//     //     .attr("class", "comment");

//     var node = document.createElement('div');   // Create a <div> node
//     var para = document.createElement("P");     // Create a <p> node
//     var t = document.createTextNode(content);   // Create a text node
//     node.setAttribute("class", "comment");      // Set the <div> to class="comment"
//     node.appendChild(para);                     // Append the <p> to <div>
//     para.appendChild(t);                        // Append the text to <p>
//     document.getElementById("comment-page").appendChild(node);  // Append the whole <div> to #comment-page

//     // node
//     //     .append("p")
//     //     .html(content)

    

//     // msg_list.push({"Comment": content})

//     // $.get(
//     //     url="admin",
//     //     data={"Comment":content}, 
//     //     success=function(data) {
//     //        console.log('page content: ' + data);
//     //     }
//     // );

//     // $.getJSON('/admin', {
//     //     wordlist: JSON.stringify(content)
//     // }, function(data){
//     //     console.log(data.result)
//     //     $( "#result" ).text(data.result);
//     // });


//     // An idea to iterate through all comments and push an object to sqlite
//     // comment.forEach(function(){

        
//     //     let message = d3.selectAll("p").text()
//     //     msg_list.push({"Comment":message})
        
//     // })
//     // //

//     document.getElementById('content').value = '';

    // console.log(msg_list)
}

function rate_comment(){
    d3.json("/model").then(function(data){
        comment = document.querySelectorAll("div.comment");
        
    })

}



