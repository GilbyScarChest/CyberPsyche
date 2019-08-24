// comment = document.getElementsByClassName("comment");
// comment = d3.selectAll(".comment");


function Steven(){
    d3.json("/model").then(function(data) {
        comment = document.querySelectorAll("div.comment");
        console.log(comment)
                for(i=0; i < data.length; i++) {

                    if (data[i] == 1) {
                        comment[i].style.background = "red";
                        //console.log(comment[i]);
                    }
                    

                }
    });
    
}
