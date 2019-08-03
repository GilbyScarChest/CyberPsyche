comment = document.querySelectorAll(".comment");


function Steven(){
    d3.json("/model").then(function(data) {
                for(i=0; i < data.length; i++) {

                    if (data[i] == 1) {
                        comment[i].style.background = "red";
                        //console.log(comment[i]);
                    }
                    

                }
    });
    
}
