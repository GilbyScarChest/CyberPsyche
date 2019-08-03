var body = d3.select('body');
var table = d3.select('table');
var thead = d3.select('thead');
var tbody = d3.select('tbody');
const fetch = window.fetch.bind(window);


// Read from csv file
// d3.csv("{{url_for('Resources', filename='Test_Twitter_Comments.csv')}}").then(function(data){
// d3.csv("Resources", "Test_Twitter_Comments.csv",function(error,data) {
d3.csv("/static/Resources/Test_Twitter_Comments.csv", function(data, error) {
   
    console.log(error)

    let row = tbody.append("tr");

    Object.entries(data).forEach(function([key, value]) {
        
        let cell = row.append("td");
        cell.text(value);

    });

    // tbody.selectAll("tr").each(function() {
    //     //console.log(this.querySelector("td:nth-child(3)").innerHTML)

    //     if(this.querySelector('td:nth-child(3)').innerHTML == 1){
    //         $(this).addClass("bully")
    //     }

    //     else{
    //         $(this).addClass("positive")
    //     }
    // })

    $(function(){
        $("tbody > tr").each(function(){
          var col_val = $(this).find("td:eq(1)").text();
          if (col_val == 1){
            $(this).addClass('bully');  //the selected class colors the row red//
          } else {
            $(this).addClass('positive');
          }
        });
      });

    
});

// var myform = $('#myTable');
// var model = 0;

// $('#runModel').click(function() {
//     $("thead > tr").append('<th>Model Score</th>');
//     myform.find('tr').each(function() {
//         var trow = $(this);
//         trow.append('<td>'+ model +'</td>');
//     })

//     $(function(){
//         $("tbody > tr").each(function(){
//           var col_val = $(this).find("td:eq(3)").text();
//           if (col_val == 1){
//             $(this).removeClass().addClass('bully');  //the selected class colors the row red//
//           } else {
//             $(this).removeClass().addClass('positive');
//           }
//         });
//       });
// });


