import logo from './logo.svg';
import { Autocomplete, TextField, CircularProgress } from "@mui/material";
import { useEffect, useState } from 'react';
// import axios from "axios";
// import DOMPurify from "dompurify";
import './App.css';


// useEffect(
//   () => {

//   },
//   []
// );

function SearchBar() {
  const [fileOptions, setFileOptions] = useState(["Pirates of the Carribean", "Mr. Bob Marley"]);
  const [loading, setLoading] = useState(false);
  return (
    <div className="max-w-lg mx-auto p-4">
      <Autocomplete
        options={fileOptions}
        loading={loading} 
        renderInput={(params) => {
          // console.log(params.InputProps)
          return (
            <TextField
              {...params}
              label="Search HTML Files"
              className="w-full"
              InputProps={{
                ...params.InputProps,
                endAdornment: (
                  <>
                    {loading ? <CircularProgress color="inherit" size={20} /> : null}
                    {params.InputProps.endAdornment}
                  </>
                ),
              }}
            />
          )
        }}
      >

      </Autocomplete>
    </div>
    
  );
}

export default SearchBar;
