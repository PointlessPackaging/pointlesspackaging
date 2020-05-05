$(document).ready(function () {
	var endpoint = '/api/chart_data/'
	var defaultData = []
	var labels = [];
	var backgroundColor = [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)'
	];
	var borderColor = [
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)'
	]
	$.ajax({
		method: "GET",
		url: endpoint,
		success: function (data) {
			packagersData = data.packagers
		    packagersCountData = data.packagersCount
			monthsData = data.months
			monthsCountData = data.monthsCount
			plasticData = data.plastic
			plasticCountData = data.plasticCount
			topPackagersData = data.topPackagers
			topPackagersCountData = data.topPackagersCount
			worstPackagersData = data.worstPackagers
			worstPackagersCountData = data.worstPackagersCount
			setChart()
		},
		error: function (error_data) {
			console.log("error")
			console.log(error_data)
		}
	})

	function setChart() {
		var ctx1 = document.getElementById("myChart1");
		var ctx2 = document.getElementById("myChart2");
		var ctx3 = document.getElementById("myChart3");
		var ctx4 = document.getElementById("myChart4");

		var myChart1 = new Chart(ctx1, {
			type: 'polarArea',
			data: {
				labels: packagersData,
				datasets: [{
					label: '# of Pointless Packaging',
					data: packagersCountData,
					backgroundColor: backgroundColor,
					borderColor: borderColor,
					borderWidth: 1
				}]
			},
			options: {
				scales: {
					yAxes: [{
						ticks: {
							beginAtZero: true
						}
					}]
				}
			}
		});

		var myChart = new Chart(ctx2, {
			type: 'horizontalBar',
			data: {
				labels: packagersData,
				datasets: [{
					label: '# of Pointless Packaging',
					data: packagersCountData,
					backgroundColor: backgroundColor,
					borderColor: borderColor,
					borderWidth: 1
				}]
			},
			options: {
				scales: {
					yAxes: [{
						ticks: {
							beginAtZero: true
						}
					}]
				}
			}
		});

		var myChart3 = new Chart(ctx3, {
			type: 'line',
			data: {
				labels: monthsData,
				datasets: [{
					label: '# of Pointless Packaging',
					data: monthsCountData,
					backgroundColor: backgroundColor,
					borderColor: borderColor,
					borderWidth: 1
				}]
			},
			options: {
				scales: {
					yAxes: [{
						ticks: {
							beginAtZero: true
						}
					}]
				}
			}
		});

        var myChart4 = new Chart(ctx4, {
			type: 'polarArea',
			data: {
				labels: plasticData,
				datasets: [{
					label: '# of Pointless Packaging',
					data: plasticCountData,
					backgroundColor: backgroundColor,
					borderColor: borderColor,
					borderWidth: 1
				}]
			},
			options: {
				scales: {
					yAxes: [{
						ticks: {
							beginAtZero: true
						}
					}]
				}
			}
		});
	}
});
