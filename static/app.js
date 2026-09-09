let revenueChart, regionChart;

function money(v){return new Intl.NumberFormat("en-IN",{style:"currency",currency:"INR",maximumFractionDigits:0}).format(v||0)}
function toast(msg){
  const el=document.getElementById("toast"); el.textContent=msg; el.style.display="block";
  setTimeout(()=>el.style.display="none",3500);
}
async function loadAnalytics(){
  const r=await fetch("/api/analytics"); const data=await r.json();
  if(!data.available) return;
  document.getElementById("revenue").textContent = money(data.total_revenue);
  const labels=data.daily_revenue.map(x=>x.date.slice(5));
  const values=data.daily_revenue.map(x=>x.revenue);
  if(revenueChart) revenueChart.destroy();
  revenueChart=new Chart(document.getElementById("revenueChart"),{
    type:"line",data:{labels,datasets:[{label:"Revenue",data:values,tension:.35,fill:true,borderWidth:2}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,grid:{color:"#eef2f7"}},x:{grid:{display:false}}}}
  });
  const rl=data.regional.map(x=>x.region), rv=data.regional.map(x=>x.revenue);
  if(regionChart) regionChart.destroy();
  regionChart=new Chart(document.getElementById("regionChart"),{
    type:"doughnut",data:{labels:rl,datasets:[{data:rv,borderWidth:0}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:"bottom"}}}
  });
}
document.getElementById("runBtn").addEventListener("click",async()=>{
  const b=document.getElementById("runBtn"); b.disabled=true; b.textContent="Running…";
  try{
    const r=await fetch("/run",{method:"POST"}); const data=await r.json();
    if(data.ok){toast("Pipeline completed. PDF report generated."); await loadAnalytics(); setTimeout(()=>location.reload(),900);}
    else toast(data.message||"Pipeline failed.");
  }catch(e){toast("Could not run the pipeline.");}
  finally{b.disabled=false;b.textContent="Run pipeline";}
});
loadAnalytics();
