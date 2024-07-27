<script lang="ts">
	import { onMount } from 'svelte';
	import { getContext } from 'svelte';
	import LineChart from '$lib/components/chart/LineChart.svelte';
	import BarChart from '$lib/components/chart/BarChart.svelte';
	import PieChart from '$lib/components/chart/PieChart.svelte';
	import { page } from '$app/stores';
	const i18n = getContext('i18n');
	let data: any[] = [];
	let demo = [
		{
			date: 2015,
			sector: 'Ngôn ngữ Hàn',
			value: 177
		},
		{
			date: 2016,
			sector: 'Ngôn ngữ Hàn',
			value: 188
		},
		{
			date: 2017,
			sector: 'Ngôn ngữ Hàn',
			value: 194
		},
		{
			date: 2018,
			sector: 'Ngôn ngữ Hàn',
			value: 185
		},
		{
			date: 2019,
			sector: 'Ngôn ngữ Hàn',
			value: 193
		},
		{
			date: 2020,
			sector: 'Ngôn ngữ Hàn',
			value: 194
		},
		{
			date: 2021,
			sector: 'Ngôn ngữ Hàn',
			value: 206
		},
		{
			date: 2022,
			sector: 'Ngôn ngữ Hàn',
			value: 219
		},
		{
			date: 2023,
			sector: 'Ngôn ngữ Hàn',
			value: 208
		},
		{
			date: 2024,
			sector: 'Ngôn ngữ Hàn',
			value: 229
		}
	];
	let year: number = 2024;
	let inputSector: string = 'Kỹ thuật phần mềm';
	let sectors: string[] = [];
	let loading: boolean = false;
	let error: string | null = null;

	let aiAns: string;
	let input: string;
	let prompLoading: boolean = false;
	let promtData = [
		{
			name: '<5',
			value: 19912018
		},
		{
			name: '5-9',
			value: 20501982
		},
		{
			name: '10-14',
			value: 20679786
		},
		{
			name: '15-19',
			value: 21354481
		},
		{
			name: '20-24',
			value: 22604232
		},
		{
			name: '25-29',
			value: 21698010
		},
		{
			name: '30-34',
			value: 21183639
		},
		{
			name: '35-39',
			value: 19855782
		},
		{
			name: '40-44',
			value: 20796128
		},
		{
			name: '45-49',
			value: 21370368
		},
		{
			name: '50-54',
			value: 22525490
		},
		{
			name: '55-59',
			value: 21001947
		},
		{
			name: '60-64',
			value: 18415681
		},
		{
			name: '65-69',
			value: 14547446
		},
		{
			name: '70-74',
			value: 10587721
		},
		{
			name: '75-79',
			value: 7730129
		},
		{
			name: '80-84',
			value: 5811429
		},
		{
			name: '≥85',
			value: 5938752
		}
	];
	async function handleClick() {
		try {
			prompLoading = true;
			const response = await fetch('http://localhost:8000/prompt-report/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Accept: 'application/json'
				},
				body: JSON.stringify({ input_text: input })
			});
			if (!response.ok) {
				throw new Error('Network response was not ok');
			}
			promtData = await response.json();
		} catch (error) {
			console.error('Error fetching data:', error);
		} finally {
			prompLoading = false; // Set loading to false after data fetch
		}
	}
	async function handleChange(event: Event) {
		input = (event.target as HTMLSelectElement).value;
		try {
			prompLoading = true;
			const response = await fetch('http://localhost:8000/prompt-report/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Accept: 'application/json'
				},
				body: JSON.stringify({ input_text: input })
			});
			if (!response.ok) {
				throw new Error('Network response was not ok');
			}
			promtData = await response.json();
		} catch (error) {
			console.error('Error fetching data:', error);
		} finally {
			prompLoading = false; // Set loading to false after data fetch
		}
	}

	async function fetchData() {
		loading = true;
		error = null;

		try {
			const res_sectors = await fetch(`http://localhost:8000/sectors`);
			const res_sectors_json = await res_sectors.json();
			sectors = res_sectors_json.sectors;

			const res = await fetch(`http://localhost:8000/search?=sectors=${inputSector}`);
			demo = await res.json();

			const response = await fetch(`http://localhost:8000/search`);

			data = await response.json();

			console.log(sectors);
		} catch (err) {
			error = (err as Error).message;
		} finally {
			loading = false;
		}
	}
	async function handleSectorChange(event: Event) {
		inputSector = (event.target as HTMLSelectElement).value;
		try {
			const res = await fetch(`http://localhost:8000/search?sectors=${inputSector}`);
			demo = await res.json();
		} catch (err) {
			error = (err as Error).message;
		}
	}
	// Fetch data on mount
	onMount(() => {
		fetchData();
	});
</script>

<div class="mb-3 flex justify-between items-center">
	<div class="text-lg font-semibold self-center">Biểu đồ</div>
</div>

{#if error}
	<div class="text-red-500">{error}</div>
{/if}

{#if !loading && data.length > 0}
	<LineChart {data} />

	<div class="mt-3 flex justify-between items-center">
		<div class="text-lg font-semibold self-center">Ngành học</div>
		<select bind:value={inputSector} on:change={handleSectorChange}>
			{#each sectors as sector}
				<option value={sector}>{sector}</option>
			{/each}
		</select>
	</div>
	<BarChart data={demo} />
{/if}

<div class="mt-3 flex items-center">
	<div class="text-lg font-semibold self-center">Tìm hiểu xu hướng</div>
	<input bind:value={input} on:change={handleChange} class="border-solid border-[1px]" />
	<button on:click={handleClick}>xác nhận</button>
</div>
{#if prompLoading}
	<div class="loading">Loading...</div>
{/if}
{#if !prompLoading}
	<PieChart data={promtData} />
{/if}
