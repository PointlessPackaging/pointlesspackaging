$(document).ready(function () {
	var endpoint = '/api/table_data/'
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
		var ctx5 = document.getElementById("myChart5");
		var ctx6 = document.getElementById("myChart6");

        var myChart5 = new Chart(ctx5, {
			type: 'bar',
			data: {
				labels: topPackagersData,
				datasets: [{
					label: 'Scores of Top Packagers',
					data: topPackagersCountData,
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

        var myChart6 = new Chart(ctx6, {
			type: 'bar',
			data: {
				labels: worstPackagersData,
				datasets: [{
					label: 'Scores of Worst Packagers',
					data: worstPackagersCountData,
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