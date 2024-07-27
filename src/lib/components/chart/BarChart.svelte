<script>
	import * as d3 from 'd3';

	// Receive plot data as prop.
	export let data;

	// The chart dimensions and margins as optional props.
	export let width = 1248;
	export let height = 600;
	export let marginTop = 80;
	export let marginRight = 0;
	export let marginBottom = 70;
	export let marginLeft = 60;

	$: console.log(data);
	// Create the x (horizontal position) scale.
	const xScale = d3
		.scaleBand()
		.domain(
			// Sort the data in descending frequency
			d3.groupSort(
				data,
				([d]) => -d.value,
				(d) => d.date
			)
		)
		.range([marginLeft, width - marginRight])
		.padding(0.1);

	// Create the y (vertical position) scale.
	const yScale = d3
		.scaleLinear()
		.domain([0, d3.max(data, (d) => d.value)])
		.range([height - marginBottom, marginTop]);
</script>

<svg {width} {height} viewBox="0 0 {width} {height}" style:max-width="100%" style:height="auto">
	<!-- Add a rect for each bar. -->
	<g fill="steelblue">
		{#each data as d}
			<rect
				x={xScale(d.date)}
				y={yScale(d.value)}
				height={yScale(0) - yScale(d.value)}
				width={xScale.bandwidth()}
			/>
		{/each}
	</g>

	<!-- X-Axis -->
	<g transform="translate(0,{height - marginBottom})">
		<line stroke="currentColor" x1={marginLeft - 6} x2={width} />

		{#each data as d}
			<!-- X-Axis Ticks -->
			<line
				stroke="currentColor"
				x1={xScale(d.date) + xScale.bandwidth() / 2}
				x2={xScale(d.date) + xScale.bandwidth() / 2}
				y1={0}
				y2={6}
			/>

			<!-- X-Axis Tick Labels -->
			<text
				fill="currentColor"
				text-anchor="middle"
				x={xScale(d.date) + xScale.bandwidth() / 2}
				y={22}
			>
				{d.date}
			</text>
		{/each}

		<!-- X-Axis Label -->
		<text fill="currentColor" x={width / 2} y={50}>{data[0].sector}</text>
	</g>

	<!-- Y-Axis -->
	<g transform="translate({marginLeft},0)">
		{#each yScale.ticks(8) as tick}
			<!-- 
          Y-Axis Ticks. 
          Note: First tick is skipped since the x-axis already acts as a tick. 
        -->
			{#if tick !== 0}
				<line stroke="currentColor" x1={0} x2={-6} y1={yScale(tick)} y2={yScale(tick)} />
			{/if}

			<!-- Y-Axis Tick Labels -->
			<text fill="currentColor" text-anchor="end" dominant-baseline="middle" y={yScale(tick)}>
				{tick}
			</text>
		{/each}
	</g>
</svg>
