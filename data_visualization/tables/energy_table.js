// Import libraries
import React, { useState, useEffect } from 'eact';
import { useTable, useSortBy, useFilters } from 'eact-table';
import { DataTable } from 'eact-data-components';
import MaterialTable from 'aterial-table';

// Create energy consumption table using React Table
function EnergyTableReactTable({ data }) {
  const [tableData, setTableData] = useState(data);
  const {
    getTableProps,
    getTheadProps,
    getTrProps,
    getThProps,
    getTdProps,
    headerGroups,
    rows,
    prepareRow
  } = useTable({ columns, data: tableData });

  useEffect(() => {
    setTableData(data);
  }, [data]);

  return (
    <table {...getTableProps()} className="energy-table">
      <thead>
        {headerGroups.map(headerGroup => (
          <tr {...getTrProps({ headerGroup })}>
            {headerGroup.headers.map(column => (
              <th {...getThProps({ column })}>{column.Header}</th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody>
       {rows.map((row, i) => {
          prepareRow(row);
          return (
            <tr {...getTrProps({ row })}>
              {row.cells.map(cell => (
                <td {...getTdProps({ cell })}>{cell.value}</td>
              ))}
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}

// Create energy consumption table using DataTables
function EnergyTableDataTables({ data }) {
  const tableRef = React.createRef();

  useEffect(() => {
    $(tableRef.current).DataTable({
      data: data,
      columns: [
        { title: 'Date' },
        { title: 'Energy Consumption (kWh)' }
      ]
    });
  }, [data]);

  return (
    <table ref={tableRef} className="energy-table">
      <thead>
        <tr>
          <th>Date</th>
          <th>Energy Consumption (kWh)</th>
        </tr>
      </thead>
      <tbody>
        {data.map(row => (
          <tr>
            <td>{row.date}</td>
            <td>{row.energy_consumption}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

// Create energy consumption table using Material-UI
function EnergyTableMaterialUI({ data }) {
  const [tableData, setTableData] = useState(data);

  useEffect(() => {
    setTableData(data);
  }, [data]);

  return (
    <MaterialTable
      title="Energy Consumption Table"
      columns={[
        { title: 'Date', field: 'date' },
        { title: 'Energy Consumption (kWh)', field: 'energy_consumption' }
      ]}
      data={tableData}
    />
  );
}

// Example usage
const data = [
  { date: '2022-01-01', energy_consumption: 100 },
  { date: '2022-01-02', energy_consumption: 120 },
  { date: '2022-01-03', energy_consumption: 110 },
  //...
];

<EnergyTableReactTable data={data} />;
<EnergyTableDataTables data={data} />;
<EnergyTableMaterialUI data={data} />;
