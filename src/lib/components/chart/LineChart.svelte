<script>
	import * as d3 from 'd3';
	// Import axes-components.
	import AxisY from './AxisY.svelte';
	import AxisX from './AxisX.svelte';

	// Receive plot data as prop.
	export let data;

	const width = 1248;
	const height = 500;

	const margin = {
		top: 10,
		right: 20,
		bottom: 20,
		left: 400
	};
	$: console.log(data);
	// Declare the x (horizontal position) scale.
	$: xScale = d3
		.scaleLinear()
		.domain(d3.extent(data, (d) => d.date))
		.range([margin.left, width - margin.right]);

	// Declare the y (vertical position) scale.
	$: yScale = d3
		.scaleLinear()
		.domain([0, d3.max(data, (d) => d.value)])
		.rangeRound([height - margin.bottom, margin.top]);

	$: groupedData = data.reduce((acc, currentValue) => {
		const sector = currentValue.sector;
		if (!acc[sector]) {
			acc[sector] = [];
		}
		acc[sector].push(currentValue);
		return acc;
	}, {});

	$: arrayData = Object.keys(groupedData).map((sector) => ({
		sector,
		values: groupedData[sector]
	}));
	$: console.log(arrayData);
	const colorMapping = {
		'Công nghệ ô tô số': '#1f77b4', // Màu xanh dương
		'Trí tuệ nhân tạo': '#ff7f0e', // Màu cam
		'Kỹ thuật phần mềm': '#2ca02c', // Màu xanh lá
		'Hệ thống thông tin': '#d62728', // Màu đỏ
		'An toàn thông tin': '#9467bd', // Màu tím
		'Thiết kế mỹ thuật số': '#8c564b', // Màu nâu
		'Digital marketing': '#e377c2', // Màu hồng
		'Kinh doanh quốc tế': '#7f7f7f', // Màu xám
		'Quản trị kinh doanh': '#bcbd22', // Màu vàng
		'Quản trị dịch vụ du lịch và lữ hành': '#17becf', // Màu xanh nước biển nhạt
		'Logistic và quản lý chuỗi cung ứng': '#ffbb78', // Màu vàng nhạt
		'Tài chính': '#1f77b4', // Màu xanh dương
		'Truyền Thông đa phương tiện': '#ff7f0e', // Màu cam
		'Quan hệ công chúng': '#2ca02c', // Màu xanh lá
		'Ngôn ngữ Anh': '#d62728', // Màu đỏ
		'Ngôn ngữ Hàn': '#9467bd', // Màu tím
		'Ngôn ngữ Nhật': '#8c564b', // Màu nâu
		'Ngôn ngữ Trung': '#e377c2', // Màu hồng
		'Vi mạch bán dẫn': '#7f7f7f' // Màu xám
	};
	// Declare the line generator.
	const line = d3
		.line()
		.x((d) => xScale(d.date))
		.y((d) => yScale(d.value));
</script>

<svg {width} {height} viewBox="0 0 {width} {height}" style:max-width="100%" style:height="auto">
	<!-- Add the y-axis -->
	<AxisY {yScale} {width} {margin} />

	<!-- Add the x-axis -->
	<AxisX {xScale} {height} {margin} />

	<!-- Add a path for the line. -->
	<g class="data">
		{#each arrayData as sectorData}
			<path fill="none" stroke={colorMapping[sectorData.sector]} d={line(sectorData.values)} />
		{/each}
	</g>
	<g class="legend" transform="translate(30, 20)">
		{#each Object.keys(colorMapping) as sector, index}
			<g transform={`translate(0, ${index * 20})`}>
				<rect width="18" height="18" fill={colorMapping[sector]} />
				<text x="25" y="9" dy=".35em" fill="currentColor">{sector}</text>
			</g>
		{/each}
	</g>
</svg>
