function fetch_data(){
    const URL='workshop.txt'
    fetch(URL)
       .then(response=>
       {
         if(!response.ok){
            throw new Error ("network was not ok");
        }
        return response.text();
         
       })
       .then(data =>{
        const line=data.trim().split("\n");

        const workshopData=[];

        line.forEach(line => {
            const [workshop,college,branch,StudentName]= line.split(',').map(item=>item.trim());
            workshopData.push({workshop,college,branch,StudentName});
        });

        const tablebody=document.getElementById('workshopdatatable');

        workshopData.forEach(entry=>{
            const row=tablebody.insertRow();
            const workshopcell=row.insertcell(0);
            const collegecell=row.insertcell(1);
            const branchcell=row.insertcell(2);
            const StudentNameCell=row.insertcell(3);

            workshopcell.textContent=entry.workshop;
            collegecell.textContent=entry.college;
            branchcell.textContent=entry.branch;
            StudentNameCell.textContent=entry.StudentName;
        });

       })

        .catch(error=>{
            console.error("there was a problem");
        });
       
    }


    fetch_data();
