# Load the qcalc package
read("//Mac/Home/Documents/qcalc.mpl");
with(qcalc);

# Function to delete old file if it exists
delete_file := proc(filename)
    if FileTools[Exists](filename) then
        FileTools[Remove](filename);
    end if;
end proc;

# Define the output file name
outfile_name := "results.csv";

# Delete the old file if it exists
delete_file(outfile_name);

# Open file to write results
outfile := fopen(outfile_name, WRITE);

# Function to write results to file
write_results := proc(space, k, n, h, sc, result)
    local outstr;
    outstr := cat(space, "(", k, ",", n, ");qmult;", 
                  convert(h, string), ";", convert(sc, string), ";", 
                  convert(result, string), "\n");
    fprintf(outfile, "%s", outstr);  # Ensure the output string is correctly formatted and printed
end proc;

# Loop through OG(2,4) to OG(2,12)
for n from 2 to 12 do
    for k from 1 to n-1 do
        try
            # Set the Grassmannian OG(2, n)
            print("OG", k, n);
            OG(k, n);
            get_type();
            # Loop through generators and Schubert classes
            for h in generators() do
                for sc in schub_classes() do
                    # Compute the qmult
                    result := qmult(h, sc);
                    # Write to file
                    write_results("OG", k, n, h, sc, result);
                end do;
            end do;
        catch e:
            print("Error in OG", k, n, ": ", e);
        end try;

        # If n is even, also set IG(2, n)
        if n mod 2 = 0 then
            try
                print("IG", k, n);
                IG(k, n);
                get_type();
                # Loop through generators and Schubert classes
                for h in generators() do
                    for sc in schub_classes() do
                        # Compute the qmult
                        result := qmult(h, sc);
                        # Write to file
                        write_results("IG", k, n, h, sc, result);
                    end do;
                end do;
            catch e:
                print("Error in IG", k, n, ": ", e);
            end try;
        end if;
    end do;
end do;

# Close the file
fclose(outfile);
