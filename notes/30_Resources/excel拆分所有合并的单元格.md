#r/tools/Excel

- Sub UnmergeAllCells()
      Dim rng As Range
      Dim cell As Range
  
      '遍历所有使用的单元格
      For Each rng In ActiveSheet.UsedRange
          If rng.MergeCells Then
              rng.UnMerge
              '如果拆分后，原合并单元格中有数据，则将数据填充到拆分后的所有单元格
              For Each cell In rng
                  cell.Value = rng.Value
              Next cell
          End If
      Next rng
  End Sub