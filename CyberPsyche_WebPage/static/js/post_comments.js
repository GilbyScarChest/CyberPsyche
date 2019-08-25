

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
// }


$("div .comment").click(function() {
    var index = $("div .comment").index(this);
    var comment_text = $(this).children('p').text();
    var current_comment = $(this);
    var rating;
    var new_rating;
    console.log(this)
    d3.json("/model").then(function(data){

        console.log(data[index])
        console.log(comment_text)
        // console.log($('.comment > p').text().index)

        if (data[index] == 0){
            rating = "Appropriate"
        }
        else{
            rating = "Inappropriate"
        }


        if (confirm(`The AI model's rating for this comment is: ${rating}\n Should it be changed?`)) {
            if (rating == "Appropriate"){
                new_rating = 1;
                console.log(`new rating changed to ${new_rating}`);
            }
            else if (rating == "Inappropriate"){
                new_rating = 0;
                console.log(`new rating changed to ${new_rating}`);
            };

            
            obj = {"Comment": comment_text, "Rating": new_rating};
            console.log(obj);
            
            $.ajax({
                // url: "{{url_for('admin')}}",
                url: "admin",
                type: "POST",
                data: obj,
                dataType: "json",
                complete: alert("Thanks for making our algorythm stronger!")
            })
            
        } 
        else{
            alert("Request for change cancelled.")
        }

        // color_change = new_rating;
        console.log(current_comment)
        // console.log(color_change)
        if (new_rating == 1){
            current_comment[0].style.background = "red";
        }
        else if (new_rating == 0){
            current_comment[0].style.background = "white";
        };
        
        
    })
});

// function colorChange(){

// }


