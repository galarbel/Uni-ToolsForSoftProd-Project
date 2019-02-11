method Append(input: array<int>,value: int) returns (result: array<int>)
{
  
  if(input != null)
  {
      result := new int[input.Length + 1];
      result[input.Length] := value;
      var index := 0; 
      while index < input.Length
      {
        result[index] := input[index];
        index := index + 1; 
      }

      return result;
  }
}

method Remove(input: array<int>,value: int) returns (result: array<int>)
{
  
  if(input != null)
  {
    if(input.Length > 0)
    {
      var flag := 0;
      result := new int[input.Length - 1];
    
      var index_result := 0; 
      var index_input := 0;
      while ((index_input < input.Length) && (index_result < result.Length))
      {
        if(input[index_input] == value && flag == 0)
        {
          index_input := index_input + 1;
          flag := 1;
        }
        if(index_input < input.Length)
        {
          result[index_result] := input[index_input];
        }
        
        index_input := index_input + 1;
        index_result := index_result + 1;
        
      }
      return result;
    }
  }
}

method len(input: array<int>) returns (result: int)
requires input != null 
{
  return input.Length;
}

method round(num: real) returns (res: int) 
  ensures res == num.Floor || res == num.Floor + 1 
{
  var tmp := num - (num.Floor as real);
  
  if tmp < 0.5 {
    return num.Floor;
  }  
  return num.Floor + 1;
}