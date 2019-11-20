function refreshHeatmap(){
		var input = $("#heatmapDate").val();
		$("#iframe3").attr("src","/home/ubuntu/analysis/poppulation/result/areaAnalysis"+input+".html")
	}